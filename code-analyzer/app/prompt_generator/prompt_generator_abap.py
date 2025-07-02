from langchain_core.documents.base import Document
from langchain_core.prompt_values import PromptValue
from langchain_core.prompts import PromptTemplate
from typing import ClassVar, List, Self


class PromptGeneratorABAP:
    _instance: ClassVar[Self | None] = None

    def __new__(cls) -> Self:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if not hasattr(self, "_initialized"):
            self._initialized: bool = True

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

    def create_batch_summary_prompt(
        self,
        file_name: str,
        batch_index: int,
        total_batches: int,
        chunk_analyses: List[Document],
    ) -> PromptValue:
        """
        Create a prompt for summarizing a batch of chunk analyses.
        Used in hierarchical summarization approach.
        """
        # Combine chunk analyses in this batch
        batch_analyses_text: str = ""
        for i, analysis in enumerate(chunk_analyses, 1):
            batch_analyses_text = batch_analyses_text + (f"\n--- Analysis {i} ---\n{analysis.page_content}\n")

        prompt = PromptTemplate(
            input_variables=[
                "file_name",
                "batch_index",
                "total_batches",
                "batch_size",
                "batch_analyses_text",
            ],
            template=self._batch_summary_prompt_template,
        )

        return prompt.invoke(
            {
                "file_name": file_name,
                "batch_index": batch_index,
                "total_batches": total_batches,
                "batch_size": len(chunk_analyses),
                "batch_analyses_text": batch_analyses_text,
            }
        )

    def create_file_summary_prompt(
        self,
        file_name: str,
        chunk_analyses: List[Document],
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

    def create_final_summary_prompt(
        self,
        file_name: str,
        intermediate_summaries: List[str],
    ) -> PromptValue:
        """
        Create a prompt for combining intermediate summaries into a final comprehensive summary.
        Used as the final step in hierarchical summarization.
        """
        # Combine intermediate summaries
        summaries_text: str = ""
        for i, summary in enumerate(intermediate_summaries, 1):
            summaries_text = summaries_text + (f"\n--- Intermediate Summary {i} ---\n{summary}\n")

        prompt = PromptTemplate(
            input_variables=[
                "file_name",
                "total_summaries",
                "intermediate_summaries_text",
            ],
            template=self._final_summary_prompt_template,
        )

        return prompt.invoke(
            {
                "file_name": file_name,
                "total_summaries": len(intermediate_summaries),
                "intermediate_summaries_text": summaries_text,
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
        return """
        You are an expert ABAP developer. Analyze the code chunk and summarize in a tabular format

        File: {file_name}
        Chunk: {chunk_index}/{total_chunks}

        Code:
        {chunk_content}

        Keep the response comprehensive but concise.
        """

    @property
    def _batch_summary_prompt_template(self) -> str:
        return """
            You are an expert ABAP developer. Create an intermediate summary for this batch of code analyses.

            File: {file_name}
            Batch: {batch_index}/{total_batches}
            Analyses in this batch: {batch_size}

            Chunk Analyses in this Batch:
            {batch_analyses_text}

            Create a concise intermediate summary focusing on:
            - Main functionality covered in this batch
            - Key components and methods
            - Important business logic
            - Data structures and interfaces
            - Notable patterns or implementations

            This will be combined with other batch summaries, so focus on the unique aspects of this batch.
            Keep the response detailed but structured for easy combination later.
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
    def _final_summary_prompt_template(self) -> str:
        return """
            You are an expert ABAP developer. Create a comprehensive final summary by combining these intermediate summaries.

            File: {file_name}
            Number of Intermediate Summaries: {total_summaries}

            Intermediate Summaries to Combine:
            {intermediate_summaries_text}

            Create a comprehensive final summary that includes:
            - Overall purpose and functionality of the entire file
            - Complete list of key components and their relationships
            - Full business logic overview
            - System integration points and interfaces
            - Technical architecture and design patterns
            - Data flow and processing logic
            - Any notable features or complex implementations

            Ensure the summary is:
            1. Comprehensive yet concise
            2. Well-structured and easy to understand
            3. Eliminates redundancy between intermediate summaries
            4. Maintains technical accuracy
            5. Provides actionable insights for developers

            Present the information in a logical flow that tells the complete story of what this code file does.
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
