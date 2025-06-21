from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_core.documents.base import Document
from pathlib import Path
from typing import ClassVar, Dict, List, Self


class Document_Loader_ABAP:
    _instance: ClassVar[Self | None] = None

    def __new__(cls) -> Self:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if not hasattr(self, "_initialized"):
            self._initialized: bool = True
            # self._directory: Dict[str, Path] = {}
            self._directory: Path
            self._code_files: List[Document] = []

    def load_directory(self, directories: Dict[str, Path]) -> List[Document]:
        if self._validate_directories(directories=directories):
            return self._load_code_documents(code_path=str(self._directory.absolute()))
        else:
            return []

    def _load_code_documents(self, code_path: str) -> List[Document]:
        try:
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
            return self._code_files
        except Exception as error:
            raise RuntimeError(f"Error loading documents: {error}")

    def _validate_directories(self, directories: Dict[str, Path]) -> bool:
        if not directories:
            raise TypeError("Directory parameter cannot be None or empty")

        if not isinstance(directories, dict):
            raise TypeError("Directory parameter must be a dictionary")

        required_keys: set[str] = {"code"}
        provided_keys: set[str] = set(directories.keys())
        missing_keys: set[str] = required_keys - provided_keys

        if missing_keys:
            raise ValueError(f"Dictionary must have 'code'. Missing keys: {', '.join(sorted(missing_keys))}")
        else:
            # self._directory["code"] = directories["code"].resolve()
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
