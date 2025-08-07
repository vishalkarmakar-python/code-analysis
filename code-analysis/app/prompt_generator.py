"""
Generates structured prompts for the Language Model.

This module defines the `PromptGenerator` class, which is responsible for
creating detailed and context-rich prompts. A well-structured prompt is
critical for guiding the LLM to produce accurate and consistently formatted
responses.
"""

from langchain_core.documents.base import Document
from langchain_core.prompt_values import PromptValue
from langchain_core.prompts import PromptTemplate
from textwrap import dedent
from typing import ClassVar, Self


class PromptGenerator:
    """
    A singleton class to create and manage prompt templates for the LLM.
    """

    _instance: ClassVar[Self | None] = None

    def __new__(cls) -> Self:
        """Ensures only one instance of PromptGenerator is created."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        """Initializes the PromptGenerator instance."""
        if not hasattr(self, "_initialized"):
            self._initialized: bool = True

    def create_analysis_prompt(
        self,
        file_name: str,
        document_type: str,
        document: Document,
        document_index: int,
        total_chunks: int,
    ) -> PromptValue:
        """
        Creates a formatted prompt for analyzing a single code chunk.

        Args:
            file_name: The name of the original source file.
            document_type: The guessed ABAP object type for context.
            document: The `Document` chunk to be analyzed.
            document_index: The index of this chunk (e.g., 1).
            total_chunks: The total number of chunks for the file.

        Returns:
            A `PromptValue` object ready to be sent to the LLM.
        """
        prompt = PromptTemplate(
            input_variables=["file_name", "chunk_type", "chunk_index", "total_chunks", "chunk_content"],
            template=self._analysis_prompt_template,
        )
        return prompt.invoke(
            {
                "file_name": file_name,
                "chunk_type": document_type,
                "chunk_index": document_index,
                "total_chunks": total_chunks,
                "chunk_content": document.page_content,
            }
        )

    @property
    def _analysis_prompt_template(self) -> str:
        """
        The master template for the code analysis prompt.

        This multi-line string defines the role, context, instructions, and
        desired output format for the LLM. The `{variable}` placeholders are
        filled in by the `create_analysis_prompt` method. `dedent` is used to
        remove leading whitespace from the string.
        """
        # Since you're an SAP expert, this prompt is tailored to leverage that persona.
        # It asks the LLM to act as a senior ABAP developer.
        return dedent("""
        You are a senior SAP ABAP developer with over 20 years of experience, specializing in S/4HANA, ABAP on HANA, and the ABAP RESTful Application Programming Model (RAP). Your expertise is deep and practical.
        Your task is to analyze the provided ABAP code chunk and generate a detailed, structured analysis.

        **Context:**
        - File Name: {file_name}
        - Suspected Object Type: {chunk_type}
        - Current Chunk: {chunk_index} of {total_chunks}

        **ABAP Code Chunk to Analyze:**
        ```abap
        {chunk_content}
        ```

        **Instructions:**
        Carefully analyze the code provided in the chunk. Based ONLY on the code in this chunk, provide the following structured analysis. If a section is not applicable or information is not present in this specific chunk, explicitly state "Not present in this chunk."

        ---

        ### 1. Object Identification and Core Purpose
        - **Object Type:** (Identify the most specific ABAP object type you can from this chunk. Examples: Global Class Definition, CDS View Entity, Behavior Definition, Report Program, Function Module, etc.)
        - **Purpose:** (Describe the primary business or technical purpose of the code in this chunk. What does it do?)

        ---

        ### 2. Detailed Technical Analysis
        - **Key Logic & Flow:** (Explain the step-by-step logic. If it's a method, describe its algorithm. If it's a CDS view, explain the joins and fields. If it's a BDEF, list the actions/determinations.)
        - **Data Interaction:** (List database tables or CDS views being read or modified. Specify the operation, e.g., `SELECT FROM SFLIGHT`, `MODIFY ENTITY /DMO/Travel`.)
        - **Dependencies:** (List any explicit calls to other objects like classes, function modules, or CDS views seen in this chunk.)
        - **Interface (if applicable):** (For classes or function modules, describe the parameters (importing, exporting, changing) or method signatures found in this chunk.)

        ---

        Generate a concise and technically accurate response based strictly on the provided code chunk. Do not invent details not present in the code.
        """)
