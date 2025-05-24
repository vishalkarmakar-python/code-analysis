"""
ABAP Code Document Generator

A Streamlit web application for uploading ABAP code files (.txt format) and generating
comprehensive documentation from them. The application provides file information display,
processing statistics, and documentation generation capabilities.

Features:
- Multiple file upload support
- File information display in tabular format
- Processing statistics and file type breakdown
- Configurable output format selection (.docx, .pdf, .md)
- Responsive layout with side-by-side columns

Author: Development Team
Created: 2025
Framework: Streamlit
"""

import streamlit as st
from app.ai_model import Llama3
from app.document_loader import TextFilesLoader
from langchain_core.documents.base import Document
from os import getcwd, path
from pandas import DataFrame
from streamlit.delta_generator import DeltaGenerator
from streamlit.runtime.uploaded_file_manager import UploadedFile
from typing import Any, Dict, List

# Configure the Streamlit page with title, icon, and wide layout
st.set_page_config(page_title="Document Generator", page_icon="📁", layout="wide")

# Main application header
st.title("📁 ABAP Code Document Generator")
st.markdown("Upload the ABAP code files and generate documentation.")

# File Upload Section - At the Top
st.subheader("File Upload")

# File uploader component that accepts multiple .txt files
# Returns List[UploadedFile] when files are selected, None when no files
uploaded_files: List[UploadedFile] | None = st.file_uploader(
    label="Choose files",
    type=[".txt", ".abap"],  # Accept only .txt file types for ABAP code
    accept_multiple_files=True,  # Enable multiple file selection
    help="Select one or more files to upload",
)

# Visual separator between sections
st.markdown("---")

# Create two columns for File Information and Process Files side by side
# Type annotations for the column objects returned by st.columns()
file_information_column: DeltaGenerator
process_files_column: DeltaGenerator
# Split the layout into 2:1 ratio - File Info gets more space than Process Files
file_information_column, process_files_column = st.columns([2, 1])

# Initialize list to store file information dictionaries
file_info_list: List[Any] = []

# Left Column - File Information Display
with file_information_column:
    st.subheader("File Information")

    # Check if files have been uploaded
    if uploaded_files:
        # Process each uploaded file to extract metadata
        for uploaded_file in uploaded_files:
            # Create dictionary with file details for each uploaded file
            file_info_list.append(
                {
                    "file_name": uploaded_file.name,  # Original filename
                    "file_path": path.join(
                        getcwd(),
                        "document_generator",
                        "code_files",
                        uploaded_file.name,
                    ),  # Full path
                    "file_size (KB)": f"{uploaded_file.size / (1024):.2f}",  # File size in KB
                    "file_type": uploaded_file.type,  # MIME type
                }
            )

        # Create and configure DataFrame for tabular display
        data_frame: DataFrame = DataFrame(data=file_info_list)
        data_frame.index = data_frame.index + 1  # Start index from 1 instead of 0
        data_frame.index.name = "Serial No."  # Name the index column
        # Display the DataFrame with full container width
        st.dataframe(data_frame, use_container_width=True)
    else:
        # Show informational message when no files are uploaded
        st.info("No files uploaded yet. Please upload files to view information.")

# Right Column - Process Files Statistics and Actions
with process_files_column:
    st.subheader("Process Files")

    # Check if files have been uploaded for processing
    if uploaded_files:
        # Calculate file statistics
        total_files_count: int = len(uploaded_files)  # Count of uploaded files
        total_size: float = sum(file.size for file in uploaded_files) / (1024 * 1024)  # Total size in MB

        # Display key metrics using Streamlit metric components
        st.metric("Total Files", total_files_count, delta=None)
        st.metric("Total Size", f"{total_size:.2f} MB", delta=None)

        # Analyze and display file type breakdown
        file_types: Dict[Any, Any] = {}  # Dictionary to store file type counts
        for file in uploaded_files:
            # Get file type or default to "Unknown" if not available
            file_type: str = file.type or "Unknown"
            # Count occurrences of each file type
            file_types[file_type] = file_types.get(file_type, 0) + 1

        # Display file type breakdown
        st.write("**File Types:**")
        for file_type, count in file_types.items():
            st.write(f"• {file_type}: {count}")

        # Show success status indicating files are ready for processing
        st.success("✅ Files ready for processing")
    else:
        # Show guidance when no files are uploaded
        st.info("No files uploaded yet.")
        st.write("📤 Upload files to see processing options.")

# Visual separator between main content and documentation generation
st.markdown("---")

# Generate Documentation Section - Only visible when files are uploaded
if uploaded_files:
    # Output Format Selection Section
    st.subheader("Select Output Format")

    # Create columns for output format selection (1:4 ratio for compact layout)
    output_format_column: DeltaGenerator
    blank_column: DeltaGenerator
    output_format_column, blank_column = st.columns([1, 4])

    # Place the output format selector in the first column
    with output_format_column:
        # Dropdown for selecting documentation output format
        output_format: str = st.selectbox(
            label="Output Format",
            options=[".docx", ".pdf", ".md"],  # Available output formats
        )

    # Documentation Generation Section
    st.subheader("Generate Documentation")

    # Create columns for generate button (1:4 ratio for compact layout)
    generate_button_column: DeltaGenerator
    blank_column: DeltaGenerator
    generate_button_column, blank_column = st.columns([1, 4])

    # Place the generate button in the first column
    with generate_button_column:
        # Primary action button for starting documentation generation
        if st.button(
            label="Generate Documentation",
            key="generate_docs",  # Unique key for the button
            disabled=False,  # Button is enabled when files are present
            use_container_width=True,  # Fill the column width
            help="Click to generate documentation for the uploaded files",
        ):
            # Show success message when documentation generation is triggered
            text_loader: TextFilesLoader = TextFilesLoader()
            documents: List[Document] = text_loader.get_text_loaders(file_list=file_info_list)
            if documents:
                ollama: Llama3 = Llama3()
                if ollama.connect():
                    # Placeholder for actual documentation generation logic
                    # For now, we just simulate success
                    st.success("Connected to Ollama server successfully.")
                st.success(
                    body=f"Documentation generation started for {len(documents)} files in {output_format} format.\n use: http://localhost:12434/api/generate for calling the Model API"
                )


else:
    # Show warning message when no files are uploaded
    st.warning("Please upload files first to generate documentation.")
