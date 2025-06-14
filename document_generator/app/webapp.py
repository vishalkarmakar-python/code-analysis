import streamlit as st
import time
from dcoument_splitter import DocumentSplitter
from document_loader import DocumentLoader
from generate_prompt import PromptGenerator
from langchain_core.documents.base import Document
from langchain_core.messages.base import BaseMessage
from langchain_core.prompt_values import PromptValue
from llm_ollama import Ollama
from os import getcwd
from streamlit import (
    button,
    columns,
    error,
    expander,
    info,
    json,
    markdown,
    set_page_config,
    spinner,
    subheader,
    success,
    text_area,
    text_input,
    title,
    warning,
    write,
)
from typing import List

# Set the page configuration for the Streamlit app
set_page_config(page_title="ABAP Document Generator", page_icon="📁", layout="wide", initial_sidebar_state="expanded")

# Sidebar Configuration
with st.sidebar:
    subheader("🔧 Configuration")

    # LLM Configuration
    with expander("🤖 LLM Settings", expanded=True):
        model_name = text_input("Model Name", value="gemma3:4b", help="Ollama model to use for documentation generation")

        ollama_url = text_input("Ollama URL", value="http://localhost:11434", help="Base URL for Ollama API")

        temperature = text_input("Temperature", value="0.1", help="Model temperature (0.0-1.0)")

    # Document Processing Configuration
    with expander("📄 Document Processing", expanded=False):
        chunk_size = text_input("Chunk Size", value="4096", help="Maximum size of document chunks")

        chunk_overlap = text_input("Chunk Overlap", value="0", help="Overlap between chunks")

# Main application header
title("🚀 ABAP Code Document Generator with Context Preservation")
markdown("Upload ABAP code files and specification templates to generate comprehensive technical documentation using AI.")

# File Upload Section
subheader("📂 File Configuration")

local_code_path_column, local_spec_path_column = columns([1, 1])

with local_code_path_column:
    markdown("**📝 ABAP Code Files Path**")
    local_code_path: str = text_input(
        key="id_code_files_path",
        label="Code Files Path",
        placeholder="Enter the file path for ABAP code files",
        help="Provide the path where the ABAP code files (.abap) are located",
        value=f"{getcwd()}\\document_generator\\files",
        label_visibility="collapsed",
    )

with local_spec_path_column:
    markdown("**📋 Specification Template Path**")
    local_spec_path: str = text_input(
        key="id_spec_file_path",
        label="Spec File Path",
        placeholder="Enter the file path for specification template",
        help="Provide the path where the specification template (.md) files are located",
        value=f"{getcwd()}\\document_generator\\files",
        label_visibility="collapsed",
    )

markdown("---")

# Processing Section
col1, col2, col3 = columns([2, 1, 2])

with col2:
    process_button = button(
        key="btn_submit",
        label="🔄 Generate Documentation",
        disabled=False,
        use_container_width=True,
        help="Click to generate documentation for the uploaded files",
        type="primary",
    )

# Initialize session state for storing results
if "documentation_result" not in st.session_state:
    st.session_state.documentation_result = None
if "processing_info" not in st.session_state:
    st.session_state.processing_info = None

# Main processing logic
if process_button:
    if all([local_code_path, local_spec_path]):
        with spinner("🔄 Processing documents and generating documentation..."):
            try:
                # Step 1: Load code documents
                info("📖 Loading ABAP code documents...")
                code_documents: List[Document] = DocumentLoader.load_code_documents(code_path=local_code_path)

                if not code_documents:
                    warning("⚠️ No ABAP code files found in the specified path!")
                    st.stop()

                # Step 2: Split ABAP documents
                info("✂️ Splitting ABAP documents into chunks...")
                abap_documents: List[Document] = DocumentSplitter.split_abap_documents(
                    documents=code_documents,
                    chunk_size=int(chunk_size),
                    chunk_overlap=int(chunk_overlap),
                )

                # Step 3: Load spec documents
                info("📋 Loading specification template documents...")
                spec_documents: List[Document] = DocumentLoader.load_spec_documents(spec_path=local_spec_path)

                if not spec_documents:
                    warning("⚠️ No specification template files found in the specified path!")
                    st.stop()

                # Step 4: Split spec documents
                info("✂️ Splitting specification documents into chunks...")
                markdown_documents: List[Document] = DocumentSplitter.split_spec_documents(
                    documents=spec_documents,
                    chunk_size=int(chunk_size),
                    chunk_overlap=int(chunk_overlap),
                )

                # Step 5: Generate prompt
                info("🎯 Generating LLM prompt...")
                prompt_generator: PromptGenerator = PromptGenerator()
                generated_prompt: PromptValue = prompt_generator.create_prompt(
                    markdown_documents=markdown_documents,
                    abap_documents=abap_documents,
                )

                # Step 6: Initialize LLM and generate response
                info("🤖 Initializing LLM and generating documentation...")
                llm_instance: Ollama = Ollama(
                    model_name=model_name,
                    url=ollama_url,
                )

                result: BaseMessage = llm_instance.generate_response(prompt=generated_prompt)

                # Store results in session state
                st.session_state.documentation_result = result
                st.session_state.processing_info = {
                    "code_docs": len(code_documents),
                    "abap_chunks": len(abap_documents),
                    "spec_docs": len(spec_documents),
                    "spec_chunks": len(markdown_documents),
                    "model_used": model_name,
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                }

                success("✅ Documentation generation completed successfully!")

            except Exception as error_message:
                error(f"❌ Error during processing: {str(error_message)}")
                st.stop()
    else:
        error("❌ Please provide both code files path and specification file path.")

# Display Results Section
if st.session_state.documentation_result:
    result = st.session_state.documentation_result
    processing_info = st.session_state.processing_info

    markdown("---")
    subheader("📊 Processing Summary")

    # Display processing statistics
    col1, col2, col3, col4 = columns(4)
    with col1:
        write(f"**📝 Code Documents:** {processing_info['code_docs']}")
    with col2:
        write(f"**✂️ ABAP Chunks:** {processing_info['abap_chunks']}")
    with col3:
        write(f"**📋 Spec Documents:** {processing_info['spec_docs']}")
    with col4:
        write(f"**✂️ Spec Chunks:** {processing_info['spec_chunks']}")

    write(f"**🤖 Model Used:** {processing_info['model_used']}")
    write(f"**⏰ Generated at:** {processing_info['timestamp']}")

    markdown("---")

    # Main documentation display
    subheader("📄 Generated Documentation")

    # Check if result.content is a string or needs processing
    if hasattr(result, "content"):
        documentation_content = result.content

        # Display the documentation content
        if isinstance(documentation_content, str):
            # Display as markdown for better formatting
            with expander("📖 View Full Documentation", expanded=True):
                markdown(documentation_content)

            # Also provide as downloadable text
            with expander("💾 Download Options", expanded=False):
                text_area(
                    "Raw Documentation Text (Copy to clipboard)",
                    value=documentation_content,
                    height=200,
                    help="You can copy this text and save it to a file",
                )

                # Add some basic statistics about the generated content
                word_count = len(documentation_content.split())
                char_count = len(documentation_content)
                line_count = len(documentation_content.splitlines())

                col1, col2, col3 = columns(3)
                with col1:
                    write(f"**Words:** {word_count}")
                with col2:
                    write(f"**Characters:** {char_count}")
                with col3:
                    write(f"**Lines:** {line_count}")

        else:
            # If it's not a string, try to display it as JSON or DataFrame
            warning("⚠️ Unexpected result format. Displaying raw content:")
            json(documentation_content)

    else:
        error("❌ No content found in the result object.")

    # Document Analysis Section
    if st.session_state.processing_info:
        markdown("---")
        with expander("🔍 Document Analysis Details", expanded=False):
            # You can add the existing analysis code here if needed
            # This would show chunk information, document explorer, etc.
            markdown("""
            **Context Preservation Features Active:**
            
            ✅ **Document Identity**: Each chunk knows which original document it came from  
            ✅ **Chunk Sequence**: Each chunk knows its position (1/3, 2/3, 3/3)  
            ✅ **Context Prefix**: Multi-chunk documents include context information  
            ✅ **Metadata Enrichment**: Rich metadata for LLM understanding  
            ✅ **Document Reconstruction**: Ability to rebuild original documents  
            ✅ **Position Indicators**: START/MIDDLE/END position markers  
            
            **Benefits for LLM Processing:**
            - LLM knows when content is partial vs complete
            - Can request related chunks from the same document
            - Better understanding of code structure and flow
            - Preserved relationships between code sections
            """)

# Footer
markdown("---")
markdown("**💡 Tips:**")
markdown("- Ensure your ABAP files have `.abap` extension")
markdown("- Specification templates should be in Markdown format (`.md`)")
markdown("- Make sure Ollama is running and accessible at the configured URL")
markdown("- For large codebases, consider processing in smaller batches")


# import pandas as pd
# from dcoument_splitter import DocumentSplitter
# from document_loader import DocumentLoader
# from generate_prompt import PromptGenerator
# from langchain_core.documents.base import Document
# from langchain_core.messages.base import BaseMessage
# from langchain_core.prompt_values import PromptValue
# from llm_ollama import Ollama
# from os import getcwd
# from streamlit import (
#     button,
#     columns,
#     dataframe,
#     error,
#     markdown,
#     set_page_config,
#     subheader,
#     success,
#     text_input,
#     title,
# )
# from streamlit.delta_generator import DeltaGenerator
# from typing import List

# # Set the page configuration for the Streamlit app
# set_page_config(page_title="Document Generator", page_icon="📁", layout="wide")

# # Main application header
# title("ABAP Code Document Generator with Context Preservation")
# markdown("Upload the ABAP code files and generate documentation with preserved context.")

# # File Upload Section - At the Top
# subheader("File Path")

# local_code_path_column: DeltaGenerator
# local_spec_path_column: DeltaGenerator

# local_code_path_column, local_spec_path_column = columns([1, 1])
# with local_code_path_column:
#     # Input field for local file path where code files are stored
#     markdown("Local Code Files Path")
#     local_code_path: str = text_input(
#         key="id_code_files_path",  # Unique key for the input field
#         label="Code Files Path",
#         placeholder="Enter the file path for the code files",
#         help="Provide the path where the code files are located",
#         value=f"{getcwd()}\\document_generator\\files",  # Default to current working directory
#     )
# with local_spec_path_column:
#     # Input field for local spec file path where template files are stored
#     markdown("Local Spec File Path")
#     local_spec_path: str = text_input(
#         key="id_spec_file_path",  # Unique key for the input field
#         label="Spec File Path",
#         placeholder="Enter the file path for the spec file",
#         help="Provide the path where the spec file is located",
#         value=f"{getcwd()}\\document_generator\\files",  # Default to current working directory
#     )
# markdown("---")

# # Create columns for generate button (1:4 ratio for compact layout)
# submit_button_column: DeltaGenerator
# blank_column: DeltaGenerator
# submit_button_column, blank_column = columns([1, 4])
# result: BaseMessage | None = None
# with submit_button_column:
#     # Primary action button for starting documentation generation
#     if button(
#         key="btn_submit",  # Unique key for the button
#         label="Submit",
#         disabled=False,  # Button is enabled when files are present
#         use_container_width=True,  # Fill the column width
#         help="Click to generate documentation for the uploaded files",
#     ):
#         if all([local_code_path, local_spec_path]):
#             try:
#                 # Load and process code documents
#                 code_documents: List[Document] = DocumentLoader.load_code_documents(code_path=local_code_path)
#                 abap_documents: List[Document] = DocumentSplitter.split_abap_documents(
#                     documents=code_documents,
#                     chunk_size=4096,
#                     chunk_overlap=0,
#                 )

#                 # Load and process spec documents
#                 spec_documents: List[Document] = DocumentLoader.load_spec_documents(spec_path=local_spec_path)
#                 markdown_documents: List[Document] = DocumentSplitter.split_spec_documents(
#                     documents=spec_documents,
#                     chunk_size=4096,
#                     chunk_overlap=0,
#                 )

#                 prompt: PromptGenerator = PromptGenerator()
#                 # Generate the prompt for documentation
#                 generated_prompt: PromptValue = prompt.create_prompt(
#                     markdown_documents=markdown_documents,
#                     abap_documents=abap_documents,
#                 )

#                 success("Documentation generation completed successfully!")
#                 if prompt and generated_prompt:
#                     llm_instance: Ollama = Ollama(
#                         model_name="gemma3:4b",
#                         url="http://localhost:11434",
#                     )

#                     result = llm_instance.generate_response(prompt=generated_prompt)

#             except Exception as error_meesage:
#                 error(f"Error during processing: {str(error_meesage)}")

#         else:
#             error("Please provide both code files path and spec file path.")

# if result:
#     markdown("### Generated Documentation")
#     # markdown(f"**Prompt:**\n```{generated_prompt}\n```")
#     # markdown(f"**Response:**\n```{result.content}\n```")
#     dataframe(
#         pd.DataFrame(result.content),
#         use_container_width=True,
#     )
