from app.document_loader.document_loader_abap import Document_Loader_ABAP
from app.document_splitter.document_splitter_abap import Document_Splitter_ABAP
from app.language_model import Gemma3
from app.prompt_generator.prompt_generator_abap import PromptGeneratorABAP
from langchain_core.documents.base import Document
from langchain_core.messages.base import BaseMessage
from langchain_core.prompt_values import PromptValue
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
        abap_documents: List[Document] = document_loader.load_directory(directories=code_directory_path)

        abap_splitter: Document_Splitter_ABAP = Document_Splitter_ABAP()
        code_files: Dict[str, List[Document]] = abap_splitter.split_documents(
            documents=abap_documents,
            chunk_size=2048,
        )
        abap_prompt: PromptGeneratorABAP = PromptGeneratorABAP()
        llm_gemma3: Gemma3 = Gemma3()
        for file_name, document_chunks in code_files.items():
            print(f"\nProcessing file: {file_name}")
            print(f"Number of chunks: {len(document_chunks)}")
            prompt: PromptValue = abap_prompt.create_code_analysis_prompt(
                file_name=file_name,
                document_chunks=document_chunks,
            )
            # print(f"Generated prompt for {file_name}:\n{prompt.to_string()}\n")
            llm_response: BaseMessage = llm_gemma3.invoke_llm(prompt=prompt)
            print(f"LLM Response for {file_name}:\n{llm_response.content}\n")

        # print("\nABAP Code Analysis Prompt:")
        # print(f"\nLoaded {len(code_files)} ABAP code chunks from the directory.")
        # print(f"\nLoaded {len(abap_documents)} ABAP code documents from the directory.")

        # Clear the directory after loading documents
        # check: bool = document_loader.clear_directory
        # print(f"\nDirectory cleared: {check}")


if __name__ == "__main__":
    main()
