from app.document_loader.document_loader_abap import Document_Loader_ABAP
from app.document_splitter.document_splitter_abap import Document_Splitter_ABAP
from app.language_model import Ollama
from app.prompt_generator.prompt_generator_abap import PromptGeneratorABAP
from app.token_manager import CL100K
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
        abap_splitter: Document_Splitter_ABAP = Document_Splitter_ABAP()
        abap_prompt: PromptGeneratorABAP = PromptGeneratorABAP()
        llm: Ollama = Ollama(model_name="GEMMA")

        abap_documents: List[Document] = document_loader.load_directory(directories=code_directory_path)
        code_files: Dict[str, List[Document]] = abap_splitter.split_documents(documents=abap_documents, chunk_size=1024)

        # Store results for each file
        file_analyses: Dict[str, List[str]] = abap_prompt.create_code_response(code_files=code_files)
        print(f"Total Files: {len(file_analyses)}")

        # Generate File Summary.
        for file_name, file_chunk in file_analyses.items():
            file_summary_prompt: PromptValue = abap_prompt.create_file_summary_prompt(
                file_name=file_name,
                chunk_analyses=file_chunk,
            )
            # Calculate total prompt tokens
            file_summary_prompt_tokens: int = CL100K.calculate_token(file_summary_prompt.to_string())
            # Send to LLM
            if llm.is_initialized:
                with llm.get_llm() as model:
                    chunk_response: BaseMessage = model.invoke(input=file_summary_prompt)
                    chunk_response_content: str = chunk_response.model_dump()["content"]
                    print(f"    LLM Response for file {file_name}:\n{chunk_response_content}\n")
                    print(f"    ✓ File {file_name} processed successfully")

        print("\nAll files processed successfully!")


if __name__ == "__main__":
    main()
