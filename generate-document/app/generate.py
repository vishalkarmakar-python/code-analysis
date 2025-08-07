from app.document_loader import Document_Loader
from app.document_splitter import Document_Splitter
from langchain_core.documents.base import Document
from pathlib import Path
from typing import ClassVar, Dict, List, Self


class Generate:
    _instance: ClassVar[Self | None] = None

    def __new__(cls) -> Self:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if not hasattr(self, "_initialized"):
            self._initialized: bool = True

    @staticmethod
    def generate_document() -> None:
        # Dummy path: path where the code files are located
        dummy_path: str = "C:\\Users\\Vishal Karmakar\\Documents\\SAP\\Artificial-Intelligence\\generate-document\\files\\backup\\"
        # Output path: path where the analyzed documents will be saved
        output_filepath: str = "C:\\Users\\Vishal Karmakar\\Documents\\SAP\\Artificial-Intelligence\\generate-document\\analyzed_documents\\"
        # Prompt user for input path
        print("Welcome to the Document Generator!")
        file_path: Path = Path(input("Enter the path for the code files: ").strip() or dummy_path)
        # Check if the file path exists
        if not file_path.exists():
            print(f"Path '{file_path}' does not exist. Using dummy path: {dummy_path}")
            file_path = Path(dummy_path)

        # Step 1: Loading Documents
        print("\n=== Step 1: Loading Documents ===")
        documents: List[Document] = Document_Loader(directories={"code": file_path}).get_code_documents

        # Step 2: Splitting Documents into Chunks
        print("\n=== Step 2: Splitting Documents into Chunks ===")
        code_files: Dict[str, List[Document]] = Document_Splitter(documents=documents, model_name="QWEN").get_documents
