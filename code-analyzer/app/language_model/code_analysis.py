from app.language_model import Ollama
from app.prompt_generator.prompt_generator_abap import PromptGeneratorABAP
from langchain_core.documents.base import Document
from langchain_core.messages.base import BaseMessage
from langchain_core.prompt_values import PromptValue
from typing import ClassVar, Dict, List, Self


class CodeAnalysis:
    _instance: ClassVar[Self | None] = None

    def __new__(cls) -> Self:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if not hasattr(self, "_initialized"):
            self._initialized: bool = True

    def code_summary_chunk_analysis(
        self,
        analysed_code_chunks: Dict[str, List[Document]],
        llm: Ollama,
    ) -> str:
        abap_prompt: PromptGeneratorABAP = PromptGeneratorABAP()

        for file_name, file_chunk in analysed_code_chunks.items():
            file_summary_prompt: PromptValue = abap_prompt.create_file_summary_prompt(
                file_name=file_name,
                chunk_analyses=file_chunk,
            )

            # Send to LLM
            if llm.is_initialized:
                with llm.get_llm() as model:
                    # Calculate total prompt tokens
                    file_summary_prompt_tokens: int = model.get_num_tokens(file_summary_prompt.to_string())
                    print(f"    Token Count of {file_name}:\n{file_summary_prompt_tokens}\n")
                    chunk_response: BaseMessage = model.invoke(input=file_summary_prompt)
                    chunk_response_content: str = chunk_response.model_dump()["content"]
                    print(f"    LLM Response for file {file_name}:\n{chunk_response_content}\n")
                    print(f"    ✓ File {file_name} processed successfully")
        return " "

    def code_chunk_analysis(
        self,
        code_files: Dict[str, List[Document]],
        llm: Ollama,
    ) -> Dict[str, List[Document]]:
        # Store results for each file
        anlyzed_files: Dict[str, List[Document]] = {}
        # Initialize PromptGeneratorABAP
        abap_prompt: PromptGeneratorABAP = PromptGeneratorABAP()
        # Process each file
        print(f"\nTotal files to process: {len(code_files)}")
        for file_name, document_chunks in code_files.items():
            anlyzed_document_chunk: str = ""
            anlyzed_document_metadata: Dict = {}
            print(f"\nProcessing file: {file_name}")
            print(f"Number of chunks: {len(document_chunks)}")

            # Process each chunk individually to stay within token limits
            for document_chunk_index, document_chunk in enumerate(document_chunks, 1):
                print(f"\nProcessing chunk {document_chunk_index}/{len(document_chunks)}")
                # Calculate tokens before sending to ensure we're within limits
                print(f"    Chunk tokens: {document_chunk.metadata['chunk_token_count']}")
                # Create prompt for single chunk
                single_chunk_prompt: PromptValue = abap_prompt.create_single_chunk_analysis_prompt(
                    file_name=file_name,
                    chunk=document_chunk,
                    chunk_index=document_chunk_index,
                    total_chunks=len(document_chunks),
                )
                # Calculate total prompt tokens
                CL100K_prompt_tokens: int = llm.get_token_count(content=single_chunk_prompt.to_string())
                print(f"    Total prompt tokens: {CL100K_prompt_tokens}")
                # Store the master metadata
                if not anlyzed_document_metadata:
                    # anlyzed_document_metadata = document_chunk.metadata.copy()
                    anlyzed_document_metadata = {
                        "source": document_chunk.metadata.get("source"),
                        "document_type": document_chunk.metadata.get("document_type"),
                        "document_id": document_chunk.metadata.get("document_id"),
                    }

                # Send to LLM
                if llm.is_initialized:
                    with llm.get_llm() as model:
                        prompt_tokens = model.get_num_tokens(text=single_chunk_prompt.to_string())
                        chunk_response: BaseMessage = model.invoke(input=single_chunk_prompt)
                        chunk_response_content: str = chunk_response.model_dump()["content"]
                        print(f"    LLM Response for chunk {document_chunk_index}:\n{chunk_response_content}\n")
                        # Store the response for this chunk
                        anlyzed_document_chunk = anlyzed_document_chunk + (f"\n{chunk_response_content}\n")
                        print(f"    ✓ Chunk {document_chunk_index} processed successfully")

            print(f"\nFile {file_name} processed with {len(anlyzed_document_chunk)} chunks.")
            # Store analyses for this file
            anlyzed_files.setdefault(
                file_name,
                [],
            ).append(
                Document(
                    metadata=anlyzed_document_metadata,
                    page_content=anlyzed_document_chunk,
                )
            )

        return anlyzed_files
