from app.language_model import Ollama
from app.language_separator import ABAP
from langchain_core.documents.base import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pathlib import Path
from typing import Any, ClassVar, Dict, List, Self


class Document_Splitter:
    _instance: ClassVar[Self | None] = None

    def __new__(cls) -> Self:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if not hasattr(self, "_initialized"):
            self._initialized: bool = True

    def split_documents(
        self,
        documents: List[Document],
        llm_instance: Ollama,
    ) -> Dict[str, List[Document]]:
        self._split_documents: Dict[str, List[Document]] = {}

        for document_index, document in enumerate(documents, 1):
            file_stem: str = Path(document.metadata.get("source", "unknown")).stem.lower()
            print(f"Processing document no-{document_index}: {file_stem}")
            # Analyze document type and adjust strategy
            document_type: str = self._analyze_document_type(document.page_content)
            print(f"\tDocument Type: {document_type}")
            document_tokens: int = llm_instance.count_tokens(content=document.page_content)
            print(f"\tDocument Token Count: {document_tokens} tokens")
            max_tokens: int = llm_instance.model_max_token
            print(f"\t{'*' * 50}")
            # Split the document
            split_document: List[Document] = self._create_splitter(
                document=document,
                chunk_size=min(document_tokens, max_tokens),
            )
            # Generate enhanced metadata
            self._split_documents[file_stem] = self._generate_context_for_document_chunks(
                llm_instance=llm_instance,
                document_metadata=document.metadata.copy(),
                document_chunks=split_document,
                document_type=document_type,
                document_tokens=document_tokens,
            )
        return self._split_documents

    def _analyze_document_type(self, content: str) -> str:
        """
        Analyze the document content to determine its primary type.
        """
        content_lower: str = content.lower()

        best_match: Dict[str, Any] = {
            "doc_type": None,
            "matched_count": 0,
            "total_keywords": 0,
            "match_percentage": 0.0,
            "matched_keywords": [],
            "missing_keywords": [],
        }

        results: List[Any] = []

        for doc_type, keywords in ABAP.DOCUMENT_KEYWORDS.items():
            # Count matching keywords
            matched_keywords: List[str] = [keyword.lower() for keyword in keywords if keyword.lower() in content_lower]
            matched_count: int = len(matched_keywords)
            total_keywords: int = len(keywords)
            match_percentage: float = matched_count / total_keywords if total_keywords > 0 else 0.0

            # Store detailed results for this doc_type
            result: Dict[str, Any] = {
                "doc_type": doc_type,
                "matched_count": matched_count,
                "total_keywords": total_keywords,
                "match_percentage": match_percentage,
                "matched_keywords": matched_keywords,
                "missing_keywords": [kw.lower() for kw in keywords if kw.lower() not in content_lower],
            }
            results.append(result)

            # Update best match if this one is better
            if match_percentage > best_match["match_percentage"]:
                best_match = result.copy()

        # Return best match only if it meets the threshold
        return best_match["doc_type"]

    def _create_splitter(
        self,
        document: Document,
        chunk_size: int,
    ) -> List[Document]:
        splitter: RecursiveCharacterTextSplitter = RecursiveCharacterTextSplitter(
            separators=ABAP.get_separators(),
            chunk_size=chunk_size,
            chunk_overlap=0,
            length_function=len,
            is_separator_regex=True,
            keep_separator=True,
        )
        split_documents: List[Document] = splitter.split_documents(documents=[document])

        return split_documents

    def _generate_context_for_document_chunks(
        self,
        llm_instance: Ollama,
        document_chunks: List[Document],
        document_type: str,
        document_metadata: Dict,
        document_tokens: int,
    ) -> List[Document]:
        """Enhanced context generation with document type awareness."""
        chunks_with_context: List[Document] = []

        for chunk_index, document_chunk in enumerate(document_chunks, 1):
            chunk_metadata: Dict[Any, Any] = document_metadata.copy()
            chunk_metadata.update(
                {
                    # Document identification
                    "document_type": document_type,
                    "document_id": Path(document_metadata.get("source", "unknown")).stem.lower(),
                    "document_tokens": document_tokens,
                    # Chunk information
                    "chunk_index": chunk_index,
                    "chunk_id": f"{Path(document_metadata.get('source', 'unknown')).stem.lower()}_chunk_{chunk_index}",
                    "chunk_token_count": llm_instance.count_tokens(content=document_chunk.page_content),
                    # Context indicators
                    "is_first_chunk": chunk_index == 1,
                    "is_last_chunk": chunk_index == len(document_chunks),
                    "is_single_chunk": len(document_chunks) == 1,
                }
            )
            chunks_with_context.append(
                Document(
                    page_content=document_chunk.page_content,
                    metadata=chunk_metadata,
                )
            )

        return chunks_with_context
