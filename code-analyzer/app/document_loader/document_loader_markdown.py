from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_core.documents.base import Document
from pathlib import Path
from typing import ClassVar, Dict, List, Self


class Document_Loader_MARKDOWN:
    _instance: ClassVar[Self | None] = None

    def __new__(cls) -> Self:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if not hasattr(self, "_initialized"):
            self._initialized: bool = True
            self._directory: Dict[str, Path] = {}
            self._code_files: List[Document] = []
            self._template_file: List[Document] = []

    def load_directory(self, directories: Dict[str, Path]) -> bool:
        if self._validate_directories(directories=directories):
            self._template_file = self._load_template_documents(template_path=str(directories["template"].absolute()))
            return True
        else:
            return False

    def _load_template_documents(self, template_path: str) -> List[Document]:
        try:
            # Load spec files from the specified directory
            return DirectoryLoader(
                path=template_path,
                glob="**/*.md",
                loader_cls=TextLoader,
                loader_kwargs={
                    "encoding": "utf-8",
                    "autodetect_encoding": True,
                },
                show_progress=True,
            ).load()
        except Exception as error:
            raise RuntimeError(f"Error loading documents: {error}")

    def _validate_directories(self, directories: Dict[str, Path]) -> bool:
        if not directories:
            raise TypeError("Directory parameter cannot be None or empty")

        if not isinstance(directories, dict):
            raise TypeError("Directory parameter must be a dictionary")

        required_keys: set[str] = {"template"}
        provided_keys: set[str] = set(directories.keys())
        missing_keys: set[str] = required_keys - provided_keys

        if missing_keys:
            raise ValueError(f"Dictionary must have 'template'. Missing keys: {', '.join(sorted(missing_keys))}")

        return True

    @property
    def is_initialized(self) -> bool:
        return self._initialized

    @property
    def get_directory(self) -> Dict[str, Path]:
        return self._directory

    @property
    def get_template_document(self) -> List[Document]:
        return self._template_file

    @property
    def clear_directory(self) -> bool:
        self._directory.clear()
        return len(self._directory) == 0
