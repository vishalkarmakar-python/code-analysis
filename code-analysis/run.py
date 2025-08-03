from app.code_analysis import Analysis
from app.create_document import CreateDocument
from app.document_loader import Document_Loader
from app.document_splitter import Document_Splitter
from app.language_model import Ollama
from app.prompt_generator import PromptGenerator
from langchain_core.documents.base import Document
from pathlib import Path
from typing import Dict, List


def main() -> None:
    dummy_path: str = "C:\\Users\\Vishal Karmakar\\Documents\\SAP\\Artificial-Intelligence\\code-analysis\\files\\backup"
    output_filepath: str = "C:\\Users\\Vishal Karmakar\\Documents\\SAP\\Artificial-Intelligence\\code-analysis\\analyzed_documents\\"

    directory: Dict[str, Path] = {}
    directory_path: Path = Path(input("\nEnter the path for the code files: ").strip() or dummy_path)

    if directory_path.exists():
        directory["code"] = directory_path

        # Step 1: Loading Documents
        print("\n=== Step 1: Loading Documents ===")
        document_loader: Document_Loader = Document_Loader()
        documents: List[Document] = document_loader.load_directory(directories=directory)
        print(f"Loaded {len(documents)} documents")
        # Step 2: Splitting Documents into Chunks
        print("\n=== Step 2: Splitting Documents into Chunks ===")
        llm_instance: Ollama = Ollama(model_name="QWEN")
        splitter: Document_Splitter = Document_Splitter()
        code_files: Dict[str, List[Document]] = splitter.split_documents(
            documents=documents,
            llm_instance=llm_instance,
        )
        print(f"Split into {len(code_files)} files with chunks")
        # Step 3: Analyzing Individual Chunks
        print("\n=== Step 3: Analyzing Individual Chunks ===")
        analysis: Analysis = Analysis()
        prompt_instance: PromptGenerator = PromptGenerator()
        # Store results for each file
        analysed_code_chunks: Dict[str, List[Document]] = analysis.chunk_analysis(
            code_files=code_files,
            prompt_instance=prompt_instance,
            llm_instance=llm_instance,
        )
        print(f"Analyzed {len(analysed_code_chunks)} files")
        # Step 4: Create Markdown Document
        print("\n=== Step 4: Create Markdown Document ===")
        create_document: CreateDocument = CreateDocument()
        if create_document.create_markdown(
            documents=analysed_code_chunks,
            output_filename=output_filepath,
        ):
            print(f"Markdown document created successfully at {output_filepath}")


if __name__ == "__main__":
    main()
