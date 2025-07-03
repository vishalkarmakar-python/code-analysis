from app.document_loader.document_loader_abap import Document_Loader_ABAP
from app.document_splitter.document_splitter_abap import Document_Splitter_ABAP
from app.language_model import CodeAnalysis, Ollama
from app.prompt_generator.prompt_generator_abap import PromptGeneratorABAP
from langchain_core.documents.base import Document
from pathlib import Path
from typing import Dict, List


def main() -> None:
    dummy_path: str = "C:\\Users\\Vishal Karmakar\\Documents\\SAP\\Artificial-Intelligence\\code-analyzer\\files"
    code_directory_path: Dict[str, Path] = {}
    code_path: Path = Path(input("\nEnter the path for the code files: ").strip() or dummy_path)
    template_directory_path: Dict[str, Path] = {}
    template_path: Path = Path(input("\nEnter the path for the template files: ").strip() or dummy_path)
    if code_path and template_path:
        code_directory_path["code"] = code_path
        template_directory_path["template"] = template_path

    if code_directory_path:
        document_loader: Document_Loader_ABAP = Document_Loader_ABAP()
        abap_splitter: Document_Splitter_ABAP = Document_Splitter_ABAP()
        abap_prompt: PromptGeneratorABAP = PromptGeneratorABAP()
        abap_code_analysis: CodeAnalysis = CodeAnalysis()
        llm: Ollama = Ollama(model_name="GEMMA")

        print("\n=== Step 1: Loading ABAP Documents ===")
        abap_documents: List[Document] = document_loader.load_directory(directories=code_directory_path)
        print(f"Loaded {len(abap_documents)} documents")

        print("\n=== Step 2: Splitting Documents into Chunks ===")
        code_files: Dict[str, List[Document]] = abap_splitter.split_documents(documents=abap_documents, chunk_size=1024)
        print(f"Split into {len(code_files)} files with chunks")

        print("\n=== Step 3: Analyzing Individual Chunks ===")
        # Store results for each file
        analysed_code_chunks: Dict[str, List[Document]] = abap_code_analysis.code_chunk_analysis(code_files=code_files, llm=llm)
        print(f"Analyzed {len(analysed_code_chunks)} files")

        print("\n=== Step 4: Creating File Summaries (with Token Management) ===")
        # Generate File Summary with hierarchical approach to handle token limits
        final_summary: str = abap_code_analysis.code_summary_chunk_analysis(analysed_code_chunks=analysed_code_chunks, llm=llm)

        print("\n" + "=" * 80)
        print("FINAL ANALYSIS SUMMARY")
        print("=" * 80)
        print(final_summary)
        print("=" * 80)

        # Optionally save the summary to a file
        try:
            output_file = Path("analysis_summary.txt")
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(final_summary)
            print(f"\n✓ Summary saved to: {output_file.absolute()}")
        except Exception as e:
            print(f"\n⚠ Warning: Could not save summary to file: {e}")

        print("\n✅ All files processed successfully!")


if __name__ == "__main__":
    main()
