"""
Handles the splitting of documents into manageable chunks for LLM processing.

This module defines the `Document_Splitter` class which takes large documents,
determines the ABAP object type based on keywords, splits them using ABAP-specific
separators, and enriches each resulting chunk with valuable metadata.
"""

from app.language_model import Ollama
from app.language_separator import ABAP
from langchain_core.documents.base import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pathlib import Path
from typing import Any, ClassVar, Dict, List, Self


class Document_Splitter:
    """
    A singleton class to split documents into context-aware chunks.

    It analyzes document content to determine the ABAP object type and then uses a
    recursive character splitter with ABAP-specific separators. Each chunk is
    then decorated with metadata about its context within the original document.
    """

    _instance: ClassVar[Self | None] = None

    def __new__(cls, documents: List[Document], model_name: str) -> Self:
        """Ensures that only one instance of Document_Splitter is created."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, documents: List[Document], model_name: str) -> None:
        """Initializes the Document_Splitter instance."""
        if not hasattr(self, "_initialized"):
            self._initialized: bool = True
            self._llm_instance: Ollama = Ollama(model_name=model_name)
            self._documents: Dict[str, List[Document]] = self._split_documents(documents=documents)

    def _split_documents(
        self,
        documents: List[Document],
    ) -> Dict[str, List[Document]]:
        """
        Splits a list of documents into a dictionary of chunked documents.

        Args:
            documents: A list of `Document` objects to be split.
            llm_instance: An initialized `Ollama` instance, used for token counting.

        Returns:
            A dictionary where keys are file stems (e.g., 'my_class') and values
            are lists of the corresponding `Document` chunks.
        """
        split_documents: Dict[str, List[Document]] = {}

        for document_index, document in enumerate(documents, 1):
            file_stem: str = Path(document.metadata.get("source", "unknown")).stem.lower()
            print(f"Processing document no-{document_index}: {file_stem}")

            # Analyze document to guess the ABAP object type.
            document_type: str = self._analyze_document_type(document.page_content)
            print(f"\tDocument Type: {document_type}")
            document_tokens: int = self._llm_instance.count_tokens(content=document.page_content)
            print(f"\tDocument Token Count: {document_tokens} tokens")
            max_tokens: int = self._llm_instance.model_max_token
            print(f"\t{'*' * 50}")

            # Split the document using an appropriate chunk size.
            split_document: List[Document] = self._create_splitter(
                document=document,
                chunk_size=min(document_tokens, max_tokens),
            )

            # Add rich context (e.g., chunk index, token count) to each chunk's metadata.
            split_documents[file_stem] = self._generate_context_for_document_chunks(
                document_metadata=document.metadata.copy(),
                document_chunks=split_document,
                document_type=document_type,
                document_tokens=document_tokens,
            )
        return split_documents

    def _analyze_document_type(self, content: str) -> str:
        """
        Analyzes the document content to determine its primary ABAP object type.

        It compares the content against a predefined dictionary of keywords for
        various ABAP objects (e.g., CLASS, ROOT ENTITY) and returns the type
        with the highest match percentage.

        Args:
            content: The string content of the document.

        Returns:
            The best-guess ABAP document type as a string (e.g., "CLASS").
        """
        content_lower: str = content.lower()
        best_match: Dict[str, Any] = {"doc_type": "GENERIC_ABAP", "match_percentage": 0.0}

        # Iterate through all known ABAP document types and their keywords.
        for doc_type, keywords in ABAP.DOCUMENT_KEYWORDS.items():
            matched_keywords: List[str] = [kw.lower() for kw in keywords if kw.lower() in content_lower]
            matched_count: int = len(matched_keywords)
            total_keywords: int = len(keywords)
            match_percentage: float = matched_count / total_keywords if total_keywords > 0 else 0.0

            # If this type is a better match than the current best, update it.
            if match_percentage > best_match["match_percentage"]:
                best_match = {"doc_type": doc_type, "match_percentage": match_percentage}

        return best_match["doc_type"]

    def _create_splitter(self, document: Document, chunk_size: int) -> List[Document]:
        """
        Creates and applies a text splitter tailored for ABAP code.

        Uses LangChain's `RecursiveCharacterTextSplitter` with a custom list of
        ABAP-specific separators (e.g., 'CLASS...DEFINITION', 'METHOD').

        Args:
            document: The `Document` to be split.
            chunk_size: The target size for each chunk.

        Returns:
            A list of `Document` objects, each representing a chunk.
        """
        splitter: RecursiveCharacterTextSplitter = RecursiveCharacterTextSplitter(
            separators=ABAP.get_separators(),
            chunk_size=chunk_size,
            chunk_overlap=0,  # No overlap to avoid redundant analysis.
            length_function=len,
            is_separator_regex=False,
            keep_separator=True,
        )
        return splitter.split_documents(documents=[document])

    def _generate_context_for_document_chunks(
        self,
        document_chunks: List[Document],
        document_type: str,
        document_metadata: Dict,
        document_tokens: int,
    ) -> List[Document]:
        """
        Enriches each document chunk with contextual metadata.

        This metadata helps the LLM understand the chunk's position and significance
        within the larger document.

        Args:
            llm_instance: The Ollama instance for token counting.
            document_chunks: The list of `Document` chunks.
            document_type: The identified ABAP object type.
            document_metadata: The original document's metadata.
            document_tokens: The total token count of the original document.

        Returns:
            A list of `Document` chunks with enhanced metadata.
        """
        chunks_with_context: List[Document] = []
        for chunk_index, document_chunk in enumerate(document_chunks, 1):
            chunk_metadata: Dict[Any, Any] = document_metadata.copy()
            chunk_metadata.update(
                {
                    "document_type": document_type,
                    "document_id": Path(document_metadata.get("source", "unknown")).stem.lower(),
                    "document_tokens": document_tokens,
                    "chunk_index": chunk_index,
                    "chunk_id": f"{Path(document_metadata.get('source', 'unknown')).stem.lower()}_chunk_{chunk_index}",
                    "chunk_token_count": self._llm_instance.count_tokens(content=document_chunk.page_content),
                    "is_first_chunk": chunk_index == 1,
                    "is_last_chunk": chunk_index == len(document_chunks),
                    "is_single_chunk": len(document_chunks) == 1,
                }
            )
            chunks_with_context.append(Document(page_content=document_chunk.page_content, metadata=chunk_metadata))
        return chunks_with_context

    @property
    def is_initialized(self) -> bool:
        return self._initialized

    @property
    def get_documents(self) -> Dict[str, List[Document]]:
        return self._documents

    @property
    def clear_documents(self) -> Dict[str, List[Document]]:
        self._documents: Dict[str, List[Document]] = {}
        return self._documents
