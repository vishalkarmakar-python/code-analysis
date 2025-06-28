from app.language_model import Ollama
from app.token_manager import CL100K
from langchain_core.documents.base import Document
from langchain_core.messages.base import BaseMessage
from langchain_core.prompt_values import PromptValue
from langchain_core.prompts import PromptTemplate
from typing import ClassVar, Dict, List, Self


class PromptGeneratorABAP:
    _instance: ClassVar[Self | None] = None

    def __new__(cls) -> Self:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if not hasattr(self, "_initialized"):
            self._initialized: bool = True

    def create_code_response(self, code_files: Dict[str, List[Document]]) -> Dict[str, List[str]]:
        # Store results for each file
        anlyzed_files: Dict[str, List[str]] = {}
        # Initialize the LLM
        llm: Ollama = Ollama(model_name="GEMMA")
        # Process each file
        print(f"\nTotal files to process: {len(code_files)}")
        for file_name, document_chunks in code_files.items():
            anlyzed_document_chunk: List[str] = []
            print(f"\nProcessing file: {file_name}")
            print(f"Number of chunks: {len(document_chunks)}")

            # Process each chunk individually to stay within token limits
            for document_chunk_index, document_chunk in enumerate(document_chunks, 1):
                print(f"\nProcessing chunk {document_chunk_index}/{len(document_chunks)}")
                # Calculate tokens before sending to ensure we're within limits
                print(f"    Chunk tokens: {document_chunk.metadata['chunk_token_count']}")
                # Create prompt for single chunk
                single_chunk_prompt: PromptValue = self.create_single_chunk_analysis_prompt(
                    file_name=file_name,
                    chunk=document_chunk,
                    chunk_index=document_chunk_index,
                    total_chunks=len(document_chunks),
                )
                # Calculate total prompt tokens
                prompt_tokens: int = CL100K.calculate_token(single_chunk_prompt.to_string())
                print(f"    Total prompt tokens: {prompt_tokens}")

                document_test: Document

                # Send to LLM
                if llm.is_initialized:
                    with llm.get_llm() as model:
                        chunk_response: BaseMessage = model.invoke(input=single_chunk_prompt)
                        chunk_response_content: str = chunk_response.model_dump()["content"]
                        print(f"    LLM Response for chunk {document_chunk_index}:\n{chunk_response_content}\n")
                        # Store the response for this chunk
                        anlyzed_document_chunk.append(chunk_response_content)
                        print(f"    ✓ Chunk {document_chunk_index} processed successfully")

            print(f"\nFile {file_name} processed with {len(anlyzed_document_chunk)} chunks.")
            # Store analyses for this file
            anlyzed_files[file_name] = anlyzed_document_chunk

        return anlyzed_files

    def create_single_chunk_analysis_prompt(
        self,
        file_name: str,
        chunk: Document,
        chunk_index: int,
        total_chunks: int,
    ) -> PromptValue:
        """
        Create a prompt for analyzing a single chunk of ABAP code.
        This helps stay within token limits.
        """
        prompt = PromptTemplate(
            input_variables=[
                "file_name",
                "chunk_index",
                "total_chunks",
                "chunk_content",
            ],
            template=self._single_chunk_prompt_template,
        )

        return prompt.invoke(
            {
                "file_name": file_name,
                "chunk_index": chunk_index,
                "total_chunks": total_chunks,
                "chunk_content": chunk.page_content,
            }
        )

    def create_file_summary_prompt(
        self,
        file_name: str,
        chunk_analyses: List[str],
    ) -> PromptValue:
        """
        Create a prompt for generating a comprehensive file summary
        based on individual chunk analyses.
        """
        # Combine all chunk analyses into a single text
        chunk_analyses_text: str = ""
        for i, analysis in enumerate(chunk_analyses, 1):
            chunk_analyses_text = chunk_analyses_text + (f"\n--- Chunk {i} ---\n{analysis}\n")

        prompt = PromptTemplate(
            input_variables=[
                "file_name",
                "total_chunks",
                "chunk_analyses_text",
            ],
            template=self._file_summary_prompt_template,
        )

        return prompt.invoke(
            {
                "file_name": file_name,
                "total_chunks": len(chunk_analyses),
                "chunk_analyses_text": chunk_analyses_text,
            }
        )

    def create_code_analysis_prompt(
        self,
        file_name: str,
        document_chunks: List[Document],
    ) -> PromptValue:
        """
        Create an enhanced prompt template that handles both ABAP code and markdown specifications.

        Returns:
            PromptTemplate configured for ABAP + Markdown processing
        """
        prompt = PromptTemplate(
            input_variables=[
                "file_name",
                "document_chunks",
            ],
            template=self._analyze_prompt_template,
        )
        return prompt.invoke(
            {
                "file_name": file_name,
                "document_chunks": document_chunks,
            }
        )

    @property
    def _single_chunk_prompt_template(self) -> str:
        # return """
        # You are an expert ABAP developer. Analyze the code chunk and provide the observation in a tabular format for:
        # - If code chunk has Class Definition or Implementation only
        # - If code chunk has CDS Root Entites Fields and Datatypes only
        # - If code chunk has Method Definition or Implementation only
        # - If code chunk has Import Parameters only
        # - If code chunk has Export Parameters only
        # - If code chunk has Changing Parameters only
        # - If code chunk has Returning Parameters only
        # - If code chunk has CDS Projection Entites Fields and Datatypes only
        # - If code chunk has CDS Behavior Definition only
        # - If code chunk has CDS Behavior Projection only
        # - If code chunk has CDS Behavior Projection only
        return """
        You are an expert ABAP developer. Analyze the code chunk and summarize in a tabular format if the chunk has: 
        - CDS Root View Entity with Fields and it's Datatypes

        File: {file_name}
        Chunk: {chunk_index}/{total_chunks}

        Code:
        {chunk_content}

        Keep the response comprehensive but concise.
    """

    @property
    def _file_summary_prompt_template(self) -> str:
        return """
            You are an expert ABAP developer. Create a comprehensive summary based on these chunk analyses.

            File: {file_name}
            Total Chunks Analyzed: {total_chunks}

            Individual Chunk Analyses:
            {chunk_analyses_text}

            Provide a comprehensive file summary including:
            - Overall purpose and functionality
            - Key components and their relationships
            - Main business logic
            - System integration points
            - Technical architecture

            Keep the response comprehensive but concise.
        """

    @property
    def _analyze_prompt_template(self) -> str:
        return """
        You are an expert ABAP developer with 15 years of experience. 
        Your task is to analyze the provided ABAP code and explain in detail what is the code about in simple language.

        ## Instructions
        - Code File Name: {file_name}
        - Code Chunks to analyze: {document_chunks}
        - Provide a detailed explanation of the code.
        - Use simple language to explain the code.
        - Do not include any code snippets in your response.
        - Focus on the functionality and purpose of the code.
        - Provide methods, function modules parameters in tabular format explaining their roles
    """
