"""
Main execution script for the ABAP Code Analysis tool.

This script orchestrates the entire code analysis pipeline:
1.  Loads ABAP source code files from a specified directory.
2.  Splits the loaded documents into manageable chunks suitable for LLM processing.
3.  Invokes a Language Model to analyze each code chunk individually.
4.  Compiles the analysis results into structured Markdown documents.

The user is prompted for a directory path, with a default path available for convenience.
"""

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
    """
    The main function to run the code analysis pipeline.

    Orchestrates the process by initializing necessary components and executing
    the steps in a sequential manner: Load -> Split -> Analyze -> Create Document.
    """
    # --- Configuration ---
    # Default path for the ABAP code files if the user provides no input.
    dummy_path: str = "C:\\Users\\Vishal Karmakar\\Documents\\SAP\\Artificial-Intelligence\\code-analysis\\files\\code"
    # Output path for the generated Markdown analysis files.
    output_filepath: str = "C:\\Users\\Vishal Karmakar\\Documents\\SAP\\Artificial-Intelligence\\code-analysis\\files\\analyzed_documents\\"

    # --- User Input ---
    directory: Dict[str, Path] = {}
    directory_path: Path = Path(input("\nEnter the path for the code files: ").strip() or dummy_path)

    if not directory_path.exists():
        print(f"Error: The specified path does not exist: {directory_path}")
        return

    directory["code"] = directory_path

    # --- Pipeline Execution ---

    # Step 1: Loading Documents
    print("\n=== Step 1: Loading Documents ===")
    document_loader: Document_Loader = Document_Loader()
    documents: List[Document] = document_loader.load_directory(directories=directory)
    if not documents:
        print("No documents found or loaded. Exiting.")
        return
    print(f"Loaded {len(documents)} documents")

    # Step 2: Splitting Documents into Chunks
    print("\n=== Step 2: Splitting Documents into Chunks ===")
    # Initialize the Ollama LLM instance. This will be used for token counting and analysis.
    llm_instance: Ollama = Ollama(model_name="QWEN")
    splitter: Document_Splitter = Document_Splitter()
    # The documents are split into a dictionary where keys are filenames and values are lists of chunked Documents.
    code_files: Dict[str, List[Document]] = splitter.split_documents(
        documents=documents,
        llm_instance=llm_instance,
    )
    print(f"Split into {len(code_files)} files with chunks")

    # Step 3: Analyzing Individual Chunks
    print("\n=== Step 3: Analyzing Individual Chunks ===")
    analysis: Analysis = Analysis()
    prompt_instance: PromptGenerator = PromptGenerator()
    # Each chunk is sent to the LLM for analysis. The results are stored in a new dictionary.
    analysed_code_chunks: Dict[str, List[Document]] = analysis.chunk_analysis(
        code_files=code_files,
        prompt_instance=prompt_instance,
        llm_instance=llm_instance,
    )
    print(f"Analyzed {len(analysed_code_chunks)} files")

    # Step 4: Create Markdown Document
    print("\n=== Step 4: Create Markdown Document ===")
    create_document: CreateDocument = CreateDocument()
    # The analyzed content is used to generate a final Markdown report for each original file.
    if create_document.create_markdown(
        documents=analysed_code_chunks,
        output_filename=output_filepath,
    ):
        print(f"Markdown document created successfully at {output_filepath}")


if __name__ == "__main__":
    main()
