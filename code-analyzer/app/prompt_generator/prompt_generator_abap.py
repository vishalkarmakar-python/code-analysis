from langchain_core.documents.base import Document
from langchain_core.prompt_values import PromptValue
from langchain_core.prompts import PromptTemplate
from typing import List


class PromptGeneratorABAP:
    _analyze_prompt_template: str = """
        You are an expert ABAP developer with 15 years of experience. 
        Your task is to analyze the provided ABAP code and explain in detail what is the code about in simple language.

        ## Instructions
        - Code File Name: {file_name}
        - Code Chunks to analyze: {document_chunks}
        - Provide a detailed explanation of the code.
        - Use simple language to explain the code.
        - Do not include any code snippets in your response.
        - Focus on the functionality and purpose of the code.
        - If the code is part of a larger system, explain its role within that system.
        - If the code is a function or method, explain its inputs, outputs, and how it fits into the overall program.
        - If the code is a class, explain its attributes, methods, and how it interacts with other classes.
        - If the code is a report, explain its purpose and how it generates output.
        - If the code is a module, explain its functionality and how it integrates with other modules.
        - If the code is a form, explain its purpose and how it is used in the application.
        - If the code is a transaction, explain its purpose and how it is used in the application.
        - If the code is a CDS view of entity, explain its purpose and how it is used in the application.
        - If the code is a RAP object, explain its purpose and how it is used in the application.        
    """

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
