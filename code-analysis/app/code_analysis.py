"""
Handles the core logic of analyzing code chunks using a Language Model.

This module defines the `Analysis` class, which takes chunked documents,
generates prompts for them, invokes the LLM, and processes the structured
output (analysis and summary) for each chunk.
"""

from app.language_model import Ollama
from app.prompt_generator import PromptGenerator
from app.structured_output import Code_Analysis
from langchain_core.documents.base import Document
from langchain_core.language_models import LanguageModelInput
from langchain_core.prompt_values import PromptValue
from langchain_core.runnables import Runnable
from pydantic import BaseModel
from typing import ClassVar, Dict, List, Self, Union


class Analysis:
    """
    A singleton class to manage the analysis of code documents.

    This class processes a dictionary of code files, where each file is a list of
    document chunks. It sends each chunk to the LLM for analysis and collects
    the structured results.
    """

    _instance: ClassVar[Self | None] = None

    def __new__(cls) -> Self:
        """Ensures that only one instance of the Analysis class is created."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        """Initializes the Analysis instance."""
        if not hasattr(self, "_initialized"):
            self._initialized: bool = True
            # Configuration for batching (not currently implemented but good for future use).
            self.MAX_TOKENS_PER_BATCH = 3000
            self.MAX_CHUNKS_PER_BATCH = 5

    def chunk_analysis(
        self,
        code_files: Dict[str, List[Document]],
        prompt_instance: PromptGenerator,
        llm_instance: Ollama,
    ) -> Dict[str, List[Document]]:
        """
        Analyzes each chunk of each document file using the LLM.

        Iterates through each file and its corresponding chunks, generates a
        specific prompt for each chunk, sends it to the LLM, and validates
        the structured response. The analysis and summary for each chunk are
        then stored as new `Document` objects.

        Args:
            code_files: A dictionary where keys are filenames and values are lists
                        of `Document` chunks.
            prompt_instance: An instance of `PromptGenerator` to create prompts.
            llm_instance: An initialized `Ollama` instance to communicate with the LLM.

        Returns:
            A dictionary where keys are filenames and values are lists of `Document`
            objects containing the analysis and summary for that file.
        """
        # Store results for each file.
        analyzed_files: Dict[str, List[Document]] = {}
        print(f"\nTotal files to process: {len(code_files)}")

        # Process each file one by one.
        for file_name, documents in code_files.items():
            analyzed_document: List[Document] = []
            analyzed_document_metadata: Dict = {}
            print(f"\nProcessing file: {file_name}")
            print(f"Type of document: {documents[0].metadata.get('document_type')}")
            print(f"Number of document chunks: {len(documents)}")

            # Process each chunk individually to stay within token limits.
            for document_chunk_index, document_chunk in enumerate(documents, 1):
                print(f"\nProcessing chunk {document_chunk_index}/{len(documents)}")
                print(f"    Chunk tokens: {document_chunk.metadata.get('chunk_token_count')}")

                # Create a detailed prompt for the current chunk.
                document_type: str = document_chunk.metadata.get("document_type", "Unknown")
                analysis_prompt: PromptValue = prompt_instance.create_analysis_prompt(
                    file_name=file_name,
                    document_type=document_type,
                    document=document_chunk,
                    document_index=document_chunk_index,
                    total_chunks=len(documents),
                )
                print(f"    Total prompt tokens: {llm_instance.count_tokens(content=analysis_prompt.to_string())}")

                # Store the master metadata from the first chunk to use for all generated documents.
                if not analyzed_document_metadata:
                    analyzed_document_metadata = document_chunk.metadata.copy()

                # Send the prompt to the LLM and get a structured response.
                with llm_instance.get_llm() as model:
                    # Chain the model with a structured output schema to enforce a predictable response format.
                    structured_model: Runnable[LanguageModelInput, Union[Dict, BaseModel]] = model.with_structured_output(schema=Code_Analysis)
                    chunk_response: Code_Analysis = Code_Analysis.model_validate(structured_model.invoke(input=analysis_prompt))

                    # Create a new Document for the 'Analysis' part of the response.
                    analysis_metadata = analyzed_document_metadata.copy()
                    analysis_metadata.update({"document_type": "Analysis"})
                    analyzed_document.append(Document(metadata=analysis_metadata, page_content=chunk_response.analysis))
                    print(f"    Analysis for File: {file_name}:\n{chunk_response.analysis}\n")

                    # Create another Document for the 'Summary' part of the response.
                    summary_metadata = analyzed_document_metadata.copy()
                    summary_metadata.update({"document_type": "Summary"})
                    analyzed_document.append(Document(metadata=summary_metadata, page_content=chunk_response.summary))
                    print(f"    Summary for File: {file_name}:\n{chunk_response.summary}\n")

            # Store the list of generated analysis/summary documents for this file.
            analyzed_files[file_name] = analyzed_document
            print(f"{'*' * 100}")

        return analyzed_files
