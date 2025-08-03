from langchain_core.documents.base import Document
from os import path
from typing import Any, ClassVar, Dict, List, Self


class CreateDocument:
    _instance: ClassVar[Self | None] = None

    def __new__(cls) -> Self:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if not hasattr(self, "_initialized"):
            self._initialized: bool = True

    def create_markdown(
        self,
        documents: Dict[str, List[Document]],
        output_filename: str,
    ) -> bool:
        success: bool = False
        # Iterate through each file and its corresponding documents
        for filename, document in documents.items():
            markdown_content: List[Any] = []
            # Add a main title to the Markdown report
            markdown_content.append("# Code Analysis Report")
            markdown_content.append("---")
            markdown_content.append(f"## File: {filename.upper()}")
            markdown_content.append("\n")
            # Process each document chunk within the file
            for document_index, document_chunk in enumerate(document, 1):
                markdown_content.append(f"### {document_index}. {document_chunk.metadata.get('document_type', 'Unknown')}")
                markdown_content.append(f"{document_chunk.page_content}")
                markdown_content.append("\n")
            # Add a separator for better readability between files
            markdown_content.append("\n---\n")
            # Write the content to the specified .md file
            try:
                with open(file=path.join(output_filename, f"{filename}.md"), mode="w", encoding="utf-8") as file:
                    file.write("\n".join(markdown_content))
                # Get the full path for the return value
                print(f"Successfully created Markdown file: {path.join(output_filename, f'{filename}.md')}")
                success = True
            except IOError as error:
                print(f"Error writing to file {path.join(output_filename, f'{filename}.md')}: {error}")
                success = False

        return success
