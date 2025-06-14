from langchain_core.documents.base import Document
from langchain_core.prompt_values import PromptValue
from langchain_core.prompts import PromptTemplate
from typing import List


class PromptGenerator:
    prompt_template: str = """
        You are an expert ABAP developer and technical documentation specialist. 
        Your task is to generate technical specification document based on the provided ABAP code and specification template.

        ## Instructions
        - Template to follow: {markdown_documents}
        - Code Files to use for generating technical specification document: {abap_documents}
    """

    def create_prompt(self, markdown_documents: List[Document], abap_documents: List[Document]) -> PromptValue:
        """
        Create an enhanced prompt template that handles both ABAP code and markdown specifications.

        Returns:
            PromptTemplate configured for ABAP + Markdown processing
        """
        prompt = PromptTemplate(
            input_variables=[
                "markdown_documents",
                "abap_documents",
            ],
            template=self.prompt_template,
        )
        return prompt.invoke(
            {
                "markdown_documents": markdown_documents,
                "abap_documents": abap_documents,
            }
        )
