from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_core.documents.base import Document
from typing import List


class DocumentLoader:
    @staticmethod
    def load_code_documents(code_path: str) -> List[Document]:
        """Load documents from the specified directories."""
        try:
            # Load code files from the specified directory
            code_loader = DirectoryLoader(
                path=code_path,
                glob="**/*.abap",
                loader_cls=TextLoader,
                loader_kwargs={
                    "encoding": "utf-8",
                    "autodetect_encoding": True,
                },
                show_progress=True,
                silent_errors=True,  # Suppress errors for missing files
            )
            code_documents: List[Document] = code_loader.load()

            return code_documents
        except Exception as error:
            raise RuntimeError(f"Error loading documents: {error}")

    @staticmethod
    def load_spec_documents(spec_path: str) -> List[Document]:
        """Load documents from the specified directories."""
        try:
            # Load spec files from the specified directory
            spec_loader = DirectoryLoader(
                path=spec_path,
                glob="**/*.md",
                loader_cls=TextLoader,
                loader_kwargs={
                    "encoding": "utf-8",
                    "autodetect_encoding": True,
                },
                show_progress=True,
            )
            spec_documents: List[Document] = spec_loader.load()

            return spec_documents
        except Exception as error:
            raise RuntimeError(f"Error loading documents: {error}")
