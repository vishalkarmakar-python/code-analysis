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

    def __new__(cls, directories: Dict[str, Path]) -> Self:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._directories: Dict[str, Path] = directories
        elif cls._directories != directories:
            print(f"[WARNING] Document_Loader singleton already initialized with directory '{cls._directories.get('code')}'. ")
        return cls._instance

    def __init__(self, directories: Dict[str, Path]) -> None:
        if not hasattr(self, "_initialized"):
            self._initialized: bool = True
            # self._directory: Dict[str, Path] = {}
            self._directory: Path
            # self._code_files: List[Document] = []
            self._code_files: List[Document] = self._load_directory(directories)

    def _load_directory(self, directories: Dict[str, Path]) -> List[Document]:
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
            print(f"Loading code files from directory: {code_path}")
            # Load code files from the specified directory
            self._code_files = DirectoryLoader(
                path=str(code_path),
                glob="**/*.abap",
                loader_cls=TextLoader,
                loader_kwargs={
                    "encoding": "utf-8",
                    "autodetect_encoding": True,
                },
                show_progress=True,
                silent_errors=True,  # Suppress errors for missing files
            ).load()
            if self._code_files:
                print(f"{len(self._code_files)} Code files loaded successfully from '{code_path}'")
                return self._code_files
            else:
                print("No code files found in the specified directory.")
                return []

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

    @property
    def is_initialized(self) -> bool:
        return self._initialized

    @property
    def get_directory(self) -> Path:
        return self._directory

    @property
    def get_code_documents(self) -> List[Document]:
        return self._code_files

    @property
    def clear_directory(self) -> bool:
        self._directory = Path()
        return self._directory == 0
