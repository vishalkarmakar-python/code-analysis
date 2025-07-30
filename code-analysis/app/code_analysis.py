from app.language_model import Ollama
from app.prompt_generator import PromptGenerator
from app.structured_output import Analysis_Chunk
from langchain_core.documents.base import Document
from langchain_core.language_models import LanguageModelInput
from langchain_core.prompt_values import PromptValue
from langchain_core.runnables import Runnable
from pydantic import BaseModel
from typing import Any, ClassVar, Dict, List, Self, Union


class CodeAnalysis:
    _instance: ClassVar[Self | None] = None

    def __new__(cls) -> Self:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if not hasattr(self, "_initialized"):
            self._initialized: bool = True
            # Token limit for safe processing (leaving room for prompt template and response)
            self.MAX_TOKENS_PER_BATCH = 3000  # Conservative limit
            self.MAX_CHUNKS_PER_BATCH = 5  # Fallback limit by chunk count

    def code_chunk_analysis(
        self,
        code_files: Dict[str, List[Document]],
        prompt_instance: PromptGenerator,
        llm_instance: Ollama,
    ) -> Dict[str, List[Document]]:
        # Store results for each file
        anlyzed_files: Dict[str, List[Document]] = {}
        # Process each file
        print(f"\nTotal files to process: {len(code_files)}")
        for file_name, documents in code_files.items():
            anlyzed_document: List[Document] = []
            anlyzed_document_metadata: Dict = {}
            anlyzed_document_content: str = ""
            print(f"\nProcessing file: {file_name}")
            print(f"Type of document: {documents[0].metadata.get('document_type')}")
            print(f"Number of document chunks: {len(documents)}")
            # Process each chunk individually to stay within token limits
            for document_chunk_index, document_chunk in enumerate(documents, 1):
                print(f"\nProcessing chunk {document_chunk_index}/{len(documents)}")
                # Calculate tokens before sending to ensure we're within limits
                print(f"    Chunk tokens: {document_chunk.metadata.get('chunk_token_count')}")
                # Create prompt for single chunk
                document_type: str = document_chunk.metadata.get("document_type", "Unknown")
                analysis_prompt: PromptValue = prompt_instance.create_analysis_prompt(
                    file_name=file_name,
                    document_type=document_type,
                    document=document_chunk,
                    document_index=document_chunk_index,
                    total_chunks=len(documents),
                )
                # Store the master metadata
                if not anlyzed_document_metadata:
                    # anlyzed_document_metadata = document_chunk.metadata.copy()
                    anlyzed_document_metadata = {
                        "source": document_chunk.metadata.get("source"),
                        "document_type": document_chunk.metadata.get("document_type"),
                        "document_id": document_chunk.metadata.get("document_id"),
                    }
                # Send to LLM
                with llm_instance.get_llm() as model:
                    print(f"    Total prompt tokens: {llm_instance.count_tokens(content=analysis_prompt.to_string())}")
                    structured_model: Runnable[LanguageModelInput, Union[Dict, BaseModel]] = model.with_structured_output(schema=Analysis_Chunk)
                    chunk_response: Dict[Any, Any] | BaseModel = structured_model.invoke(input=analysis_prompt)
                    chunk_response_structured: Analysis_Chunk = Analysis_Chunk.model_validate(chunk_response)
                    print(f"    Analysis for File: {file_name}:\n{chunk_response_structured.analysis}\n")
                    print(f"    Summary for File: {file_name}:\n{chunk_response_structured.summary}\n")
                    print(f"{'*' * 100}")
                    anlyzed_document_content = f"{chunk_response_structured.analysis} \n\n {chunk_response_structured.summary}"
                    print(f"    Chunk content: {anlyzed_document_content}")
                    anlyzed_document.append(Document(metadata=anlyzed_document_metadata, page_content=anlyzed_document_content))
                    # Store analyses for this file
                    print(f"\nFile {file_name} processed with {len(anlyzed_document_content)} chunks.")
                    anlyzed_files[file_name] = anlyzed_document
        return anlyzed_files
