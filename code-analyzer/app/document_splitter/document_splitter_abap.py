from app.language_model import Gemma3
from app.separator.language import Language_Abap
from hashlib import md5
from langchain_core.documents.base import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pathlib import Path
from typing import Any, ClassVar, Dict, List, Self


class Document_Splitter_ABAP:
    _instance: ClassVar[Self | None] = None

    def __new__(cls) -> Self:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if not hasattr(self, "_initialized"):
            self._initialized: bool = True
            # self._split_documents: Dict[str, List[Document]]
            # self._splitter: RecursiveCharacterTextSplitter

    def split_documents(
        self,
        documents: List[Document],
        chunk_size: int,
    ) -> Dict[str, List[Document]]:
        self._split_documents: Dict[str, List[Document]] = {}
        """Split ABAP code documents into smaller chunks."""
        self._splitter: RecursiveCharacterTextSplitter = self.create_abap_splitter(chunk_size=chunk_size)
        for document_index, document in enumerate(documents):
            # Generate a unique document ID based on source path and content hash
            document_name: str = Path(document.metadata["source"]).stem
            document_id: str = self._generate_document_id(document, document_index)
            document_metadata: Dict[Any, Any] = document.metadata.copy()
            token_count: int = Gemma3().calculate_token(page_content=document.page_content)
            document_chunks: List[Document] = self._splitter.split_documents(documents=[document])
            document_chunks_with_context: List[Document] = self._generate_context_for_document_chunks(
                document=document,
                document_id=document_id,
                document_metadata=document_metadata,
                document_chunks=document_chunks,
                token_count=token_count,
            )
            self._split_documents[document_name] = document_chunks_with_context

        return self._split_documents

    def create_abap_splitter(
        self,
        chunk_size: int,
    ) -> RecursiveCharacterTextSplitter:
        """Create a text splitter optimized for ABAP code."""
        return RecursiveCharacterTextSplitter(
            separators=Language_Abap.ABAP,
            chunk_size=chunk_size,
            chunk_overlap=0,
            length_function=len,
            is_separator_regex=False,
            keep_separator=True,
        )

    def _generate_document_id(
        self,
        document: Document,
        document_index: int,
    ) -> str:
        """Generate a unique document ID based on source and content."""
        # Use source path if available, otherwise use content hash
        if "source" in document.metadata:
            source_path: Any = document.metadata["source"]
            # Use filename and a short hash for readability
            filename: str = Path(source_path).stem
            content_hash: str = md5(document.page_content.encode()).hexdigest()[:8]
            return f"{filename}_{content_hash}"
        else:
            # Fallback to index and content hash
            content_hash = md5(document.page_content.encode()).hexdigest()[:8]
            return f"document_{document_index}_{content_hash}"

    def _generate_context_for_document_chunks(
        self,
        document: Document,
        document_id: str,
        document_metadata: Dict,
        document_chunks: List[Document],
        token_count: int,
    ) -> List[Document]:
        chunks_with_context: List[Document] = []
        """Add context to each document chunk."""
        for chunk_index, chunk in enumerate(document_chunks):
            chunk_metadata: Dict[Any, Any] = document_metadata.copy()
            chunk_metadata.update(
                {
                    # Document identification
                    "document_type": "abap",
                    "document_id": document_id,
                    "document_chunks": len(document_chunks),
                    "document_token_count": token_count,
                    "document_size": len(document.page_content),
                    # Chunk information
                    "chunk_index": chunk_index + 1,
                    "chunk_id": f"{document_id}_chunk_{chunk_index + 1}",
                    "chunk_token_count": Gemma3().calculate_token(page_content=chunk.page_content),
                    "chunk_size": len(chunk.page_content),
                    # Context indicators
                    "is_first_chunk": chunk_index == 0,
                    "is_last_chunk": chunk_index == len(document_chunks) - 1,
                    "is_single_chunk": len(document_chunks) == 1,
                    # Positional context
                    "chunk_position_ratio": round((chunk_index) / len(document_chunks), 2),
                }
            )
            # Add surrounding context information for better LLM understanding
            context_info: Dict = self._build_context_info(
                document_metadata=document_metadata,
                chunk_index=chunk_index + 1,
                document_id=document_id,
                document_type="abap",
                total_chunks=len(document_chunks),
            )
            # Enhance the chunk content with context prefix
            enhanced_content: str = self._add_context_prefix(
                chunk_content=chunk.page_content,
                context_info=context_info,
                chunk_index=chunk_index + 1,
                total_chunks=len(document_chunks),
            )

            # Create Document with enhanced content and metadata
            chunks_with_context.append(
                Document(
                    page_content=enhanced_content,
                    metadata=chunk_metadata,
                )
            )

        return chunks_with_context

    def _build_context_info(
        self,
        document_metadata: Dict,
        chunk_index: int,
        document_id: str,
        document_type: str,
        total_chunks: int,
    ) -> Dict:
        source_file: str = document_metadata.get("source", "unknown")
        filename: str = Path(source_file).name if source_file else "unknown"
        return {
            "source_file": filename,
            "document_id": document_id,
            "document_type": document_type.upper(),
            "chunk_position": f"{chunk_index}/{total_chunks}",
            "is_multi_chunk": total_chunks > 1,
        }

    def _add_context_prefix(
        self,
        chunk_content: str,
        context_info: dict,
        chunk_index: int,
        total_chunks: int,
    ) -> str:
        """Add context prefix to chunk content for better LLM understanding."""

        # Only add prefix for multi-chunk documents
        if not context_info["is_multi_chunk"]:
            return chunk_content

        # Create context prefix
        prefix_lines: List[str] = [
            "[DOCUMENT_CONTEXT]",
            f"Source: {context_info['source_file']}",
            f"Document ID: {context_info['document_id']}",
            f"Document Type: {context_info['document_type']}",
            f"Chunk: {context_info['chunk_position']}",
        ]

        # Add position indicators
        if chunk_index == 1:
            prefix_lines.append("Position: START of document")
        elif chunk_index == total_chunks:
            prefix_lines.append("Position: END of document")
        else:
            prefix_lines.append("Position: MIDDLE of document")

        prefix_lines.append("[/DOCUMENT_CONTEXT]")
        prefix_lines.append("")  # Empty line separator

        return "\n".join(prefix_lines) + chunk_content
