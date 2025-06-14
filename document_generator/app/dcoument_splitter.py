from hashlib import md5
from langchain_core.documents.base import Document
from langchain_text_splitters import Language, RecursiveCharacterTextSplitter
from pathlib import Path
from separators import Separators
from typing import Any, Dict, List, Literal


class DocumentSplitter:
    @staticmethod
    def split_abap_documents(
        documents: List[Document],
        chunk_size: int,
        chunk_overlap: int,
    ) -> List[Document]:
        """Split ABAP code documents into chunks with preserved context."""
        try:
            abap_splitter: RecursiveCharacterTextSplitter = DocumentSplitter.create_abap_splitter(
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
            )
            split_documents: List[Document] = []

            for doc_index, doc in enumerate(documents):
                # Generate a unique document ID based on source path and content hash
                doc_id: str = DocumentSplitter._generate_document_id(doc, doc_index)
                original_metadata: Dict[Any, Any] = doc.metadata.copy()

                # Split the document into chunks
                chunks: List[Document] = abap_splitter.split_documents([doc])

                # Enhance each chunk with context metadata
                enhanced_chunks: List[Document] = DocumentSplitter._enhance_chunks_with_context(
                    chunks=chunks, doc_id=doc_id, original_doc=doc, original_metadata=original_metadata, doc_type="abap"
                )

                split_documents.extend(enhanced_chunks)

            return split_documents
        except Exception as error:
            raise RuntimeError(f"Error splitting ABAP documents: {error}")

    @staticmethod
    def split_spec_documents(
        documents: List[Document],
        chunk_size: int,
        chunk_overlap: int,
    ) -> List[Document]:
        """Split specification/markdown documents into chunks with preserved context."""
        try:
            generic_splitter: RecursiveCharacterTextSplitter = DocumentSplitter.create_markdown_splitter(
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
            )
            split_documents: List[Document] = []

            for doc_index, doc in enumerate(documents):
                # Generate a unique document ID
                doc_id: str = DocumentSplitter._generate_document_id(doc, doc_index)
                original_metadata: Dict[Any, Any] = doc.metadata.copy()

                # Split the document into chunks
                chunks: List[Document] = generic_splitter.split_documents([doc])

                # Enhance each chunk with context metadata
                enhanced_chunks: List[Document] = DocumentSplitter._enhance_chunks_with_context(
                    chunks=chunks, doc_id=doc_id, original_doc=doc, original_metadata=original_metadata, doc_type="markdown"
                )

                split_documents.extend(enhanced_chunks)

            return split_documents
        except Exception as error:
            raise RuntimeError(f"Error splitting spec documents: {error}")

    @staticmethod
    def _generate_document_id(doc: Document, doc_index: int) -> str:
        """Generate a unique document ID based on source and content."""
        # Use source path if available, otherwise use content hash
        if "source" in doc.metadata:
            source_path: Any = doc.metadata["source"]
            # Use filename and a short hash for readability
            filename: str = Path(source_path).stem
            content_hash: str = md5(doc.page_content.encode()).hexdigest()[:8]
            return f"{filename}_{content_hash}"
        else:
            # Fallback to index and content hash
            content_hash = md5(doc.page_content.encode()).hexdigest()[:8]
            return f"doc_{doc_index}_{content_hash}"

    @staticmethod
    def _enhance_chunks_with_context(
        chunks: List[Document], doc_id: str, original_doc: Document, original_metadata: dict, doc_type: str
    ) -> List[Document]:
        """Enhance chunks with context metadata for better LLM understanding."""
        enhanced_chunks: List[Any] = []
        total_chunks: int = len(chunks)
        original_length: int = len(original_doc.page_content)

        for chunk_index, chunk in enumerate(chunks):
            # Create enhanced metadata
            enhanced_metadata: Dict[Any, Any] = original_metadata.copy()
            enhanced_metadata.update(
                {
                    # Document identification
                    "document_id": doc_id,
                    "document_type": doc_type,
                    # Chunk information
                    "chunk_index": chunk_index,
                    "total_chunks": total_chunks,
                    "chunk_id": f"{doc_id}_chunk_{chunk_index}",
                    # Size information
                    "chunk_size": len(chunk.page_content),
                    "original_document_size": original_length,
                    # Context indicators
                    "is_first_chunk": chunk_index == 0,
                    "is_last_chunk": chunk_index == total_chunks - 1,
                    "is_single_chunk": total_chunks == 1,
                    # Positional context
                    "chunk_position_ratio": round((chunk_index + 1) / total_chunks, 2),
                }
            )

            # Add surrounding context information for better LLM understanding
            context_info: Dict[Any, Any] = DocumentSplitter._build_context_info(
                chunk_index=chunk_index, total_chunks=total_chunks, doc_id=doc_id, doc_type=doc_type, original_metadata=original_metadata
            )

            # Enhance the chunk content with context prefix
            enhanced_content: str = DocumentSplitter._add_context_prefix(
                chunk_content=chunk.page_content, context_info=context_info, chunk_index=chunk_index, total_chunks=total_chunks
            )

            # Create enhanced document
            enhanced_chunk = Document(page_content=enhanced_content, metadata=enhanced_metadata)

            enhanced_chunks.append(enhanced_chunk)

        return enhanced_chunks

    @staticmethod
    def _build_context_info(chunk_index: int, total_chunks: int, doc_id: str, doc_type: str, original_metadata: dict) -> dict:
        """Build context information for the chunk."""
        source_file: Any = original_metadata.get("source", "Unknown")
        filename: str = Path(source_file).name if source_file != "Unknown" else "Unknown"

        return {
            "source_file": filename,
            "document_id": doc_id,
            "document_type": doc_type.upper(),
            "chunk_position": f"{chunk_index + 1}/{total_chunks}",
            "is_multi_chunk": total_chunks > 1,
        }

    @staticmethod
    def _add_context_prefix(chunk_content: str, context_info: dict, chunk_index: int, total_chunks: int) -> str:
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
        if chunk_index == 0:
            prefix_lines.append("Position: START of document")
        elif chunk_index == total_chunks - 1:
            prefix_lines.append("Position: END of document")
        else:
            prefix_lines.append("Position: MIDDLE of document")

        prefix_lines.append("[/DOCUMENT_CONTEXT]")
        prefix_lines.append("")  # Empty line separator

        return "\n".join(prefix_lines) + chunk_content

    @staticmethod
    def create_abap_splitter(
        chunk_size: int,
        chunk_overlap: int,
    ) -> RecursiveCharacterTextSplitter:
        """Create a text splitter optimized for ABAP code."""
        return RecursiveCharacterTextSplitter(
            separators=Separators.ABAP,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            is_separator_regex=False,
            keep_separator=True,
        )

    @staticmethod
    def create_markdown_splitter(
        chunk_size: int,
        chunk_overlap: int,
    ) -> RecursiveCharacterTextSplitter:
        """Create a generic text splitter for non-ABAP documents."""
        return RecursiveCharacterTextSplitter.from_language(
            language=Language.MARKDOWN,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            keep_separator=True,
        )

    @staticmethod
    def get_chunk_info(documents: List[Document]) -> dict:
        """Get information about the chunks created."""
        try:
            if not documents:
                return {"total_chunks": 0, "average_chunk_size": 0, "total_characters": 0}

            total_chars: int = sum(len(doc.page_content) for doc in documents)
            avg_chunk_size: float | Literal[0] = total_chars / len(documents) if documents else 0

            # Group chunks by document_id for better analysis
            docs_info: Dict[Any, Any] = {}
            for doc in documents:
                doc_id: Any = doc.metadata.get("document_id", "unknown")
                if doc_id not in docs_info:
                    docs_info[doc_id] = {
                        "chunk_count": 0,
                        "total_size": 0,
                        "document_type": doc.metadata.get(
                            "document_type",
                            "unknown",
                        ),
                    }
                docs_info[doc_id]["chunk_count"] = docs_info[doc_id]["chunk_count"] + 1
                docs_info[doc_id]["total_size"] = docs_info[doc_id]["total_size"] + len(doc.page_content)

            return {
                "total_chunks": len(documents),
                "average_chunk_size": int(avg_chunk_size),
                "total_characters": total_chars,
                "min_chunk_size": min(len(doc.page_content) for doc in documents),
                "max_chunk_size": max(len(doc.page_content) for doc in documents),
                "unique_documents": len(docs_info),
                "documents_info": docs_info,
                "multi_chunk_documents": sum(1 for info in docs_info.values() if info["chunk_count"] > 1),
            }
        except Exception as error:
            raise RuntimeError(f"Error getting chunk information: {error}")

    @staticmethod
    def get_document_ids(documents: List[Document]) -> List[str]:
        """Get all unique document IDs from the chunks."""
        return list(set(doc.metadata.get("document_id", "unknown") for doc in documents))

    @staticmethod
    def get_chunks_by_document(documents: List[Document], document_id: str) -> List[Document]:
        """Get all chunks belonging to a specific document."""
        return [doc for doc in documents if doc.metadata.get("document_id") == document_id]

    @staticmethod
    def reconstruct_document(documents: List[Document], document_id: str) -> str:
        """Reconstruct the original document content from its chunks."""
        chunks: List[Document] = DocumentSplitter.get_chunks_by_document(documents, document_id)
        if not chunks:
            return ""

        # Sort chunks by chunk_index
        sorted_chunks: List[Document] = sorted(chunks, key=lambda x: x.metadata.get("chunk_index", 0))

        # Remove context prefixes and combine content
        content_parts: List[Any] = []
        for chunk in sorted_chunks:
            content: str = chunk.page_content
            # Remove context prefix if present
            if content.startswith("[DOCUMENT_CONTEXT]"):
                lines: List[str] = content.split("\n")
                # Find the end of context section
                for i, line in enumerate(lines):
                    if line.strip() == "[/DOCUMENT_CONTEXT]":
                        # Skip context section and empty line
                        content = "\n".join(lines[i + 2 :])
                        break
            content_parts.append(content)

        return "".join(content_parts)
