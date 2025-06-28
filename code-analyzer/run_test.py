from app.language_model import Ollama
from dataclasses import dataclass
from enum import Enum
from langchain_core.documents.base import Document
from typing import Dict, List


class ProcessingStrategy(Enum):
    """Different strategies for handling large documents."""

    SINGLE_CHUNK = "single_chunk"  # Process one chunk at a time
    BATCH_CHUNKS = "batch_chunks"  # Process multiple chunks in batches
    SUMMARIZE_CHUNKS = "summarize_chunks"  # Analyze chunks then summarize
    ADAPTIVE = "adaptive"  # Choose strategy based on document size


@dataclass
class TokenLimits:
    """Token limits for different models."""

    max_context: int
    safe_limit: int  # Leave buffer for response tokens
    prompt_overhead: int  # Estimated tokens for prompt template

    @property
    def max_content_tokens(self) -> int:
        """Maximum tokens available for actual content."""
        return self.safe_limit - self.prompt_overhead


class ModelConfigurations:
    """Pre-configured token limits for common models."""

    GEMMA3_4B = TokenLimits(
        max_context=4096,
        safe_limit=3800,  # Leave 296 tokens for response
        prompt_overhead=200,  # Estimated tokens for prompt template
    )

    GEMMA3_8B = TokenLimits(max_context=8192, safe_limit=7800, prompt_overhead=200)

    LLAMA3_8B = TokenLimits(max_context=8192, safe_limit=7800, prompt_overhead=200)

    LLAMA3_70B = TokenLimits(max_context=8192, safe_limit=7800, prompt_overhead=200)


class TokenManager:
    """Utility class for managing tokens and choosing optimal strategies."""

    def __init__(self, model_config: TokenLimits):
        self.config = model_config
        self.llm = Ollama()

    def calculate_optimal_chunk_size(self, sample_text: str = "") -> int:
        """
        Calculate optimal chunk size based on model limits.

        Args:
            sample_text: Sample text to estimate character-to-token ratio
        """
        if sample_text:
            # Estimate character-to-token ratio from sample
            sample_tokens = self.llm.calculate_token(sample_text)
            char_to_token_ratio = len(sample_text) / max(sample_tokens, 1)
        else:
            # Use conservative estimate (3.5 chars per token for code)
            char_to_token_ratio = 3.5

        # Calculate chunk size that will fit within token limits
        max_chunk_tokens = self.config.max_content_tokens
        optimal_chunk_size = int(max_chunk_tokens * char_to_token_ratio * 0.9)  # 90% safety margin

        return max(optimal_chunk_size, 500)  # Minimum 500 characters

    def choose_processing_strategy(self, document: Document, target_chunk_size: int) -> ProcessingStrategy:
        """
        Choose the best processing strategy based on document characteristics.
        """
        doc_tokens = self.llm.calculate_token(document.page_content)
        doc_size = len(document.page_content)
        estimated_chunks = max(1, doc_size // target_chunk_size)

        if doc_tokens <= self.config.max_content_tokens:
            # Document fits in one request
            return ProcessingStrategy.SINGLE_CHUNK
        elif estimated_chunks <= 5:
            # Small number of chunks, process individually then summarize
            return ProcessingStrategy.SUMMARIZE_CHUNKS
        elif estimated_chunks <= 20:
            # Medium number of chunks, use adaptive batching
            return ProcessingStrategy.BATCH_CHUNKS
        else:
            # Large document, must use chunk-by-chunk with summaries
            return ProcessingStrategy.SUMMARIZE_CHUNKS

    def validate_prompt_size(self, prompt_text: str) -> tuple[bool, int, str]:
        """
        Validate if prompt fits within token limits.

        Returns:
            (is_valid, token_count, message)
        """
        token_count = self.llm.calculate_token(prompt_text)

        if token_count <= self.config.safe_limit:
            return True, token_count, "Prompt within safe limits"
        elif token_count <= self.config.max_context:
            return False, token_count, f"Prompt exceeds safe limit ({token_count} > {self.config.safe_limit})"
        else:
            return False, token_count, f"Prompt exceeds hard limit ({token_count} > {self.config.max_context})"

    def get_batch_size(self, chunk_tokens: List[int]) -> int:
        """
        Calculate how many chunks can be processed together.

        Args:
            chunk_tokens: List of token counts for each chunk
        """
        available_tokens = self.config.max_content_tokens
        batch_size = 0
        cumulative_tokens = 0

        for tokens in chunk_tokens:
            if cumulative_tokens + tokens <= available_tokens:
                cumulative_tokens += tokens
                batch_size += 1
            else:
                break

        return max(1, batch_size)  # Always process at least one chunk


class DocumentProcessor:
    """High-level document processor that uses optimal strategies."""

    def __init__(self, model_config: TokenLimits = ModelConfigurations.GEMMA3_4B):
        self.token_manager = TokenManager(model_config)
        self.config = model_config

    def get_processing_recommendations(self, documents: List[Document]) -> Dict:
        """
        Analyze documents and provide processing recommendations.
        """
        recommendations = {
            "total_documents": len(documents),
            "document_analysis": [],
            "recommended_chunk_size": None,
            "overall_strategy": None,
            "estimated_processing_time": 0,
        }

        # Analyze each document
        total_tokens = 0
        document_strategies = []

        for doc in documents:
            doc_tokens = self.token_manager.llm.calculate_token(doc.page_content)
            doc_size = len(doc.page_content)
            total_tokens += doc_tokens

            # Calculate optimal chunk size for this document
            optimal_chunk_size = self.token_manager.calculate_optimal_chunk_size(doc.page_content)
            estimated_chunks = max(1, doc_size // optimal_chunk_size)

            strategy = self.token_manager.choose_processing_strategy(doc, optimal_chunk_size)
            document_strategies.append(strategy)

            doc_analysis = {
                "source": doc.metadata.get("source", "unknown"),
                "size_chars": doc_size,
                "size_tokens": doc_tokens,
                "estimated_chunks": estimated_chunks,
                "recommended_strategy": strategy.value,
                "optimal_chunk_size": optimal_chunk_size,
            }
            recommendations["document_analysis"].append(doc_analysis)

        # Overall recommendations
        recommendations["total_tokens"] = total_tokens
        recommendations["recommended_chunk_size"] = self.token_manager.calculate_optimal_chunk_size()

        # Choose overall strategy based on majority
        strategy_counts = {}
        for strategy in document_strategies:
            strategy_counts[strategy] = strategy_counts.get(strategy, 0) + 1

        most_common_strategy = max(strategy_counts.items(), key=lambda x: x[1])[0]
        recommendations["overall_strategy"] = most_common_strategy.value

        # Estimate processing time (rough)
        total_chunks = sum(doc["estimated_chunks"] for doc in recommendations["document_analysis"])
        recommendations["estimated_chunks"] = total_chunks
        recommendations["estimated_processing_time"] = total_chunks * 30  # 30 seconds per chunk estimate

        return recommendations

    def print_recommendations(self, documents: List[Document]) -> None:
        """Print processing recommendations in a user-friendly format."""
        recs = self.get_processing_recommendations(documents)

        print(f"\n{'=' * 60}")
        print("DOCUMENT PROCESSING RECOMMENDATIONS")
        print(f"{'=' * 60}")
        print(f"Model Configuration: {self.config.max_context} max tokens, {self.config.safe_limit} safe limit")
        print(f"Total Documents: {recs['total_documents']}")
        print(f"Total Tokens: {recs['total_tokens']:,}")
        print(f"Recommended Chunk Size: {recs['recommended_chunk_size']} characters")
        print(f"Overall Strategy: {recs['overall_strategy']}")
        print(f"Estimated Chunks: {recs['estimated_chunks']}")
        print(f"Estimated Processing Time: {recs['estimated_processing_time'] // 60} minutes")

        print("\nPer-Document Analysis:")
        print(f"{'-' * 60}")
        for doc in recs["document_analysis"]:
            print(f"File: {doc['source']}")
            print(f"  Size: {doc['size_chars']:,} chars, {doc['size_tokens']:,} tokens")
            print(f"  Chunks: {doc['estimated_chunks']}")
            print(f"  Strategy: {doc['recommended_strategy']}")
            print(f"  Optimal Chunk Size: {doc['optimal_chunk_size']}")
            print()


# Example usage function
def analyze_token_requirements(documents: List[Document]) -> None:
    """Convenience function to analyze and print token requirements."""
    processor = DocumentProcessor(ModelConfigurations.GEMMA3_4B)
    processor.print_recommendations(documents)
