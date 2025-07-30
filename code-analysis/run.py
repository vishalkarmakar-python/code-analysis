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
        print("\n=== Step 1: Loading Documents ===")
        documents: List[Document] = document_loader.load_directory(directories=directory)
        print(f"Loaded {len(documents)} documents")

        llm_instance: Ollama = Ollama(model_name="QWEN")
        splitter: Document_Splitter = Document_Splitter()
        print("\n=== Step 2: Splitting Documents into Chunks ===")
        code_files: Dict[str, List[Document]] = splitter.split_documents(
            documents=documents,
            llm_instance=llm_instance,
        )
        print(f"Split into {len(code_files)} files with chunks")

        code_analysis: CodeAnalysis = CodeAnalysis()
        prompt_instance: PromptGenerator = PromptGenerator()
        print("\n=== Step 3: Analyzing Individual Chunks ===")
        # Store results for each file
        analysed_code_chunks: Dict[str, List[Document]] = code_analysis.code_chunk_analysis(
            code_files=code_files,
            prompt_instance=prompt_instance,
            llm_instance=llm_instance,
        )
        print(f"Analyzed {len(analysed_code_chunks)} files")

        # print("\n=== Step 4: Summarizing Code Analysis ===")
        # # Final results for each file
        # analysed_code_summary: str = code_analysis.code_summary_chunk_analysis(
        #     analysed_code_chunks=analysed_code_chunks,
        #     llm=Ollama(model_name="GEMMA"),
        # )
        # print(f"Analyzed {len(analysed_code_chunks)} files")


if __name__ == "__main__":
    main()
