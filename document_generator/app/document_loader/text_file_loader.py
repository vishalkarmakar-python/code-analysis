from langchain_community.document_loaders import TextLoader
from langchain_core.documents.base import Document
from typing import Any, ClassVar, List, Self


class TextFilesLoader:
    _instance: ClassVar[Self | None] = None

    def __new__(cls) -> Self:
        if cls._instance is None:
            cls._instance = super(TextFilesLoader, cls).__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        # Only initialize attributes if this is the first time __init__ is called
        if not hasattr(self, "_initialized"):
            self._initialized: bool = True
            self.text_file_list: List[Document] = []

    def get_text_loaders(self, file_list: List[Any]) -> List[Document]:
        """
        Returns the current list of TextLoader objects.

        Returns:
            List[TextLoader]: Current list of TextLoader objects
        """
        # return self.text_file_list
        if self._clear_text_loaders():
            return self._load_text_files(file_list=file_list)
        else:
            print("Error clearing text loaders")
            return []

    def _load_text_files(self, file_list: List[Any]) -> List[Document]:
        if file_list:
            for file in file_list:
                try:
                    if isinstance(file, dict) and file.get("file_path"):
                        lobj_TextLoader: TextLoader = TextLoader(
                            file_path=file["file_path"],
                            encoding="utf-8",
                            autodetect_encoding=True,
                        )
                        self.text_file_list.extend(lobj_TextLoader.load())
                except Exception as error:
                    print(f"Error creating TextLoader for file: {error}")
            return self.text_file_list
        else:
            self.text_file_list = []

        print(f"{len(self.text_file_list)} files loaded")
        return self.text_file_list

    def _clear_text_loaders(self) -> bool:
        """
        Clears the current list of TextLoader objects.
        """
        self.text_file_list.clear()
        return True
