from app.code_analysis import CodeAnalysis
from app.document_loader import Document_Loader
from app.document_splitter import Document_Splitter
from app.language_model import Ollama
from app.prompt_generator import PromptGenerator
from langchain_core.documents.base import Document
from pathlib import Path
from typing import Dict, List


def main() -> None:
    dummy_path: str = "C:\\Users\\Vishal Karmakar\\Documents\\SAP\\Artificial-Intelligence\\code-analysis\\files\\code"
    directory: Dict[str, Path] = {}
    directory_path: Path = Path(input("\nEnter the path for the code files: ").strip() or dummy_path)

    if directory_path.exists():
        directory["code"] = directory_path

        document_loader: Document_Loader = Document_Loader()
        splitter: Document_Splitter = Document_Splitter()
        code_analysis: CodeAnalysis = CodeAnalysis()

        print("\n=== Step 1: Loading Documents ===")
        documents: List[Document] = document_loader.load_directory(directories=directory)
        print(f"Loaded {len(documents)} documents")

        print("\n=== Step 2: Splitting Documents into Chunks ===")
        code_files: Dict[str, List[Document]] = splitter.split_documents(
            documents=documents,
            chunk_size=1024,
            llm_instance=Ollama(model_name="GEMMA"),
        )  # Assuming llm is not needed for this example
        print(f"Split into {len(code_files)} files with chunks")

        print("\n=== Step 3: Analyzing Individual Chunks ===")
        # Store results for each file
        analysed_code_chunks: Dict[str, List[Document]] = code_analysis.code_chunk_analysis(
            code_files=code_files,
            prompt_instance=PromptGenerator(),
            llm_instance=Ollama(model_name="GEMMA"),
        )
        print(f"Analyzed {len(analysed_code_chunks)} files")


if __name__ == "__main__":
    main()
