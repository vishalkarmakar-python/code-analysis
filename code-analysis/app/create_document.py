"""
Handles the creation of final output documents from the analysis results.

This module defines the `CreateDocument` class, which takes the structured
analysis data (a dictionary of filenames mapped to analyzed documents) and
compiles it into human-readable Markdown files.
"""

from langchain_core.documents.base import Document
from os import path
from typing import ClassVar, Dict, List, Self


class CreateDocument:
    """
    A singleton class to generate Markdown files from analyzed documents.
    """

    _instance: ClassVar[Self | None] = None

    def __new__(cls) -> Self:
        """Ensures that only one instance of CreateDocument is created."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        """Initializes the CreateDocument instance."""
        if not hasattr(self, "_initialized"):
            self._initialized: bool = True

    def create_markdown(
        self,
        documents: Dict[str, List[Document]],
        output_filename: str,
    ) -> bool:
        """
        Generates a Markdown file for each analyzed source file.

        Args:
            documents: A dictionary where keys are original filenames and values are
                       lists of `Document` objects containing the analysis and summary.
            output_filename: The directory path where the .md files will be saved.

        Returns:
            True if all files were written successfully, False otherwise.
        """
        overall_success: bool = True
        # Iterate through each original file and its corresponding analysis documents.
        for filename, doc_list in documents.items():
            markdown_content: List[str] = []

            # Start with a main title for the report.
            markdown_content.append(f"# Code Analysis Report: `{filename.upper()}`")
            markdown_content.append("---")

            # Process each generated document (which contains analysis or summary).
            for document_chunk in doc_list:
                # Use the 'document_type' from metadata as a sub-header (e.g., 'Analysis', 'Summary').
                doc_type = document_chunk.metadata.get("document_type", "Content")
                chunk_index = document_chunk.metadata.get("chunk_index", 0)

                markdown_content.append(f"## {doc_type} (from Chunk {chunk_index})")
                markdown_content.append(document_chunk.page_content)
                markdown_content.append("\n")  # Add spacing for readability.

            markdown_content.append("\n---\n")  # Separator at the end of the file.

            # Write the collected Markdown content to a file.
            output_path = path.join(output_filename, f"{filename}_analysis.md")
            try:
                with open(file=output_path, mode="w", encoding="utf-8") as file:
                    file.write("\n".join(markdown_content))
                print(f"Successfully created Markdown file: {output_path}")
            except IOError as error:
                print(f"Error writing to file {output_path}: {error}")
                overall_success = False

        return overall_success
