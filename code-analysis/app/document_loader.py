"""
Handles the loading of source code documents from the filesystem.

This module provides the `Document_Loader` class, which uses LangChain's
`DirectoryLoader` to find and load all `.abap` files from a specified
directory and its subdirectories.
"""

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_core.documents.base import Document
from pathlib import Path
from typing import ClassVar, Dict, List, Self


class Document_Loader:
    """
    A singleton class to load documents from a specified directory.

    It validates the input directory and uses `DirectoryLoader` to recursively
    load all files with the `.abap` extension.
    """

    _instance: ClassVar[Self | None] = None

    def __new__(cls) -> Self:
        """Ensures that only one instance of Document_Loader is created."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        """Initializes the Document_Loader instance."""
        if not hasattr(self, "_initialized"):
            self._initialized: bool = True
            self._directory: Path
            self._code_files: List[Document] = []

    def load_directory(self, directories: Dict[str, Path]) -> List[Document]:
        """
        Loads all `.abap` files from the given directory path.

        Args:
            directories: A dictionary that must contain a 'code' key with a
                         `Path` object pointing to the source code directory.

        Returns:
            A list of `Document` objects, where each document represents one file.
            Returns an empty list if validation fails.
        """
        if self._validate_directories(directories=directories):
            return self._load_code_documents(code_path=str(self._directory.absolute()))
        else:
            return []

    def _load_code_documents(self, code_path: str) -> List[Document]:
        """
        Internal method to perform the document loading using DirectoryLoader.

        Args:
            code_path: The absolute path to the directory to scan.

        Returns:
            A list of loaded `Document` objects.

        Raises:
            RuntimeError: If the DirectoryLoader encounters a critical error.
        """
        try:
            # Configure the loader to find .abap files, use UTF-8, and show progress.
            self._code_files = DirectoryLoader(
                path=str(code_path),
                glob="**/*.abap",  # Recursively find all .abap files
                loader_cls=TextLoader,
                loader_kwargs={"encoding": "utf-8", "autodetect_encoding": True},
                show_progress=True,
                silent_errors=True,
            ).load()
            return self._code_files
        except Exception as error:
            raise RuntimeError(f"Error loading documents: {error}")

    def _validate_directories(self, directories: Dict[str, Path]) -> bool:
        """
        Validates the input dictionary to ensure it has the required structure.

        Args:
            directories: The input dictionary to validate.

        Returns:
            True if the dictionary is valid.

        Raises:
            TypeError: If the input is not a dictionary.
            ValueError: If the dictionary is missing the 'code' key.
        """
        if not isinstance(directories, dict):
            raise TypeError("Directory parameter must be a dictionary")

        if "code" not in directories:
            raise ValueError("Dictionary must have a 'code' key.")

        self._directory = directories["code"].resolve()
        return True
