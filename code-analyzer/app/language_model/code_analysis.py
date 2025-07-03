from app.language_model.ollama import Ollama
from app.prompt_generator.prompt_generator_abap import PromptGeneratorABAP
from langchain_core.documents.base import Document
from langchain_core.messages.base import BaseMessage
from langchain_core.prompt_values import PromptValue
from typing import ClassVar, Dict, List, Self


class CodeAnalysis:
    _instance: ClassVar[Self | None] = None

    def __new__(cls) -> Self:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if not hasattr(self, "_initialized"):
            self._initialized: bool = True
            # Token limit for safe processing (leaving room for prompt template and response)
            self.MAX_TOKENS_PER_BATCH = 3000  # Conservative limit
            self.MAX_CHUNKS_PER_BATCH = 5  # Fallback limit by chunk count

    def code_summary_chunk_analysis(
        self,
        analysed_code_chunks: Dict[str, List[Document]],
        llm: Ollama,
    ) -> str:
        abap_prompt: PromptGeneratorABAP = PromptGeneratorABAP()
        final_summaries: Dict[str, str] = {}

        for file_name, file_chunk in analysed_code_chunks.items():
            print(f"\nProcessing file summary for: {file_name}")
            print(f"Total chunks to summarize: {len(file_chunk)}")

            # Check if we need to batch the chunks
            total_content_tokens: int = self._calculate_total_tokens(file_chunk, llm)
            print(f"Total content tokens: {total_content_tokens}")

            if total_content_tokens > self.MAX_TOKENS_PER_BATCH or len(file_chunk) > self.MAX_CHUNKS_PER_BATCH:
                print("    Using hierarchical summarization approach")
                file_summary: str = self._hierarchical_summarization(file_name, file_chunk, llm, abap_prompt)
            else:
                print("    Using direct summarization approach")
                file_summary = self._direct_summarization(file_name, file_chunk, llm, abap_prompt)

            final_summaries[file_name] = file_summary
            print(f"    ✓ File {file_name} summary completed")

        return self._create_overall_summary(final_summaries)

    def _calculate_total_tokens(self, chunks: List[Document], llm: Ollama) -> int:
        """Calculate total tokens for all chunks content."""
        total_tokens = 0
        for chunk in chunks:
            total_tokens += llm.get_token_count(content=chunk.page_content)
        return total_tokens

    def _hierarchical_summarization(self, file_name: str, file_chunks: List[Document], llm: Ollama, abap_prompt: PromptGeneratorABAP) -> str:
        """Process chunks in batches and create hierarchical summaries."""

        # Step 1: Create batches of chunks
        chunk_batches: List[List[Document]] = self._create_chunk_batches(file_chunks, llm)
        print(f"    Created {len(chunk_batches)} batches for processing")

        # Step 2: Create intermediate summaries for each batch
        intermediate_summaries: List[str] = []

        for batch_index, batch in enumerate(chunk_batches, 1):
            print(f"    Processing batch {batch_index}/{len(chunk_batches)}")

            batch_summary_prompt: PromptValue = abap_prompt.create_batch_summary_prompt(
                file_name=file_name,
                batch_index=batch_index,
                total_batches=len(chunk_batches),
                chunk_analyses=batch,
            )

            if llm.is_initialized:
                with llm.get_llm() as model:
                    batch_tokens: int = model.get_num_tokens(batch_summary_prompt.to_string())
                    print(f"      Batch {batch_index} tokens: {batch_tokens}")

                    batch_response: BaseMessage = model.invoke(input=batch_summary_prompt)
                    batch_summary = batch_response.model_dump()["content"]
                    intermediate_summaries.append(batch_summary)
                    print(f"      ✓ Batch {batch_index} summarized")

        # Step 3: Combine intermediate summaries into final summary
        if len(intermediate_summaries) > 1:
            print(f"    Combining {len(intermediate_summaries)} intermediate summaries")
            final_summary_prompt: PromptValue = abap_prompt.create_final_summary_prompt(
                file_name=file_name,
                intermediate_summaries=intermediate_summaries,
            )

            if llm.is_initialized:
                with llm.get_llm() as model:
                    final_tokens: int = model.get_num_tokens(final_summary_prompt.to_string())
                    print(f"      Final summary tokens: {final_tokens}")

                    final_response: BaseMessage = model.invoke(input=final_summary_prompt)
                    intermediate_summaries.append(final_response.model_dump()["content"])
            return intermediate_summaries[-1] if intermediate_summaries else ""
        else:
            return intermediate_summaries[0] if intermediate_summaries else ""

    def _direct_summarization(self, file_name: str, file_chunks: List[Document], llm: Ollama, abap_prompt: PromptGeneratorABAP) -> str:
        """Process all chunks in a single prompt (original approach)."""

        file_summary_prompt: PromptValue = abap_prompt.create_file_summary_prompt(
            file_name=file_name,
            chunk_analyses=file_chunks,
        )

        if llm.is_initialized:
            with llm.get_llm() as model:
                file_summary_prompt_tokens: int = model.get_num_tokens(file_summary_prompt.to_string())
                print(f"    Token Count of {file_name}: {file_summary_prompt_tokens}")

                chunk_response: BaseMessage = model.invoke(input=file_summary_prompt)
                chunk_response_content: str = chunk_response.model_dump()["content"]
                print(f"    LLM Response for file {file_name}:\n{chunk_response_content}\n")
                return chunk_response_content

        return ""

    def _create_chunk_batches(self, chunks: List[Document], llm: Ollama) -> List[List[Document]]:
        """Create batches of chunks that fit within token limits."""
        batches: List[List[Document]] = []
        current_batch: List[Document] = []
        current_batch_tokens = 0

        for chunk in chunks:
            chunk_tokens: int = llm.get_token_count(content=chunk.page_content)

            # Check if adding this chunk would exceed limits
            if (current_batch_tokens + chunk_tokens > self.MAX_TOKENS_PER_BATCH or len(current_batch) >= self.MAX_CHUNKS_PER_BATCH) and current_batch:
                # Save current batch and start new one
                batches.append(current_batch)
                current_batch = [chunk]
                current_batch_tokens: int = chunk_tokens
            else:
                # Add chunk to current batch
                current_batch.append(chunk)
                current_batch_tokens += chunk_tokens

        # Add the last batch if it has content
        if current_batch:
            batches.append(current_batch)

        return batches

    def _create_overall_summary(self, file_summaries: Dict[str, str]) -> str:
        """Create an overall summary of all processed files."""
        if not file_summaries:
            return "No files were processed."

        summary_parts = [
            "=== OVERALL CODE ANALYSIS SUMMARY ===",
            f"Total files processed: {len(file_summaries)}",
            f"Files: {', '.join(file_summaries.keys())}",
            "",
            "=== INDIVIDUAL FILE SUMMARIES ===",
        ]

        for file_name, summary in file_summaries.items():
            summary_parts.extend(
                [
                    "",
                    f"--- {file_name} ---",
                    summary,
                ]
            )

        return "\n".join(summary_parts)

    def code_chunk_analysis(
        self,
        code_files: Dict[str, List[Document]],
        llm: Ollama,
    ) -> Dict[str, List[Document]]:
        # Store results for each file
        anlyzed_files: Dict[str, List[Document]] = {}
        # Initialize PromptGeneratorABAP
        abap_prompt: PromptGeneratorABAP = PromptGeneratorABAP()
        # Process each file
        print(f"\nTotal files to process: {len(code_files)}")
        for file_name, document_chunks in code_files.items():
            anlyzed_document: List[Document] = []
            anlyzed_document_metadata: Dict = {}
            anlyzed_document_content: str = ""
            print(f"\nProcessing file: {file_name}")
            print(f"Number of chunks: {len(document_chunks)}")

            # Process each chunk individually to stay within token limits
            for document_chunk_index, document_chunk in enumerate(document_chunks, 1):
                print(f"\nProcessing chunk {document_chunk_index}/{len(document_chunks)}")
                # Calculate tokens before sending to ensure we're within limits
                print(f"    Chunk tokens: {document_chunk.metadata['chunk_token_count']}")
                # Create prompt for single chunk
                single_chunk_prompt: PromptValue = abap_prompt.create_single_chunk_analysis_prompt(
                    file_name=file_name,
                    chunk=document_chunk,
                    chunk_index=document_chunk_index,
                    total_chunks=len(document_chunks),
                )
                # Calculate total prompt tokens
                CL100K_prompt_tokens: int = llm.get_token_count(content=single_chunk_prompt.to_string())
                print(f"    Total prompt tokens: {CL100K_prompt_tokens}")
                # Store the master metadata
                if not anlyzed_document_metadata:
                    # anlyzed_document_metadata = document_chunk.metadata.copy()
                    anlyzed_document_metadata = {
                        "source": document_chunk.metadata.get("source"),
                        "document_type": document_chunk.metadata.get("document_type"),
                        "document_id": document_chunk.metadata.get("document_id"),
                    }

                # Send to LLM
                if llm.is_initialized:
                    with llm.get_llm() as model:
                        prompt_tokens: int = model.get_num_tokens(text=single_chunk_prompt.to_string())
                        chunk_response: BaseMessage = model.invoke(input=single_chunk_prompt)
                        chunk_response_content: str = chunk_response.model_dump()["content"]
                        print(f"    LLM Response for chunk {document_chunk_index}:\n{chunk_response_content}\n")
                        # Store the response for this chunk
                        print(f"    ✓ Chunk {document_chunk_index} processed successfully")
                        anlyzed_document_content = chunk_response_content
                        anlyzed_document.append(Document(metadata=anlyzed_document_metadata, page_content=anlyzed_document_content))

            # Store analyses for this file
            print(f"\nFile {file_name} processed with {len(anlyzed_document_content)} chunks.")
            anlyzed_files[file_name] = anlyzed_document

        return anlyzed_files
