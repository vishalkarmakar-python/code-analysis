import streamlit as st
from app.ai_model.llama3 import Llama3
from app.document_loader import TextDocumentLoader
from app.prompt.prompt_ts import Prompt
from app.schema.schema_file import SchemaFile
from app.services.process_files_streamlit import File_Processor_Streamlit
from langchain_core.documents.base import Document
from langchain_core.messages.base import BaseMessage
from os import getcwd
from streamlit.delta_generator import DeltaGenerator
from streamlit.runtime.uploaded_file_manager import UploadedFile
from typing import List

# from app.ai_model import Llama3
# from app.prompt import Prompt
# from langchain_core.documents.base import Document
# from os import getcwd, path
# from pandas import DataFrame

# Configure the Streamlit page with title, icon, and wide layout
st.set_page_config(page_title="Document Generator", page_icon="📁", layout="wide")

# Main application header
st.title("ABAP Code Document Generator")
st.markdown("Upload the ABAP code files and generate documentation.")

# File Upload Section - At the Top
st.subheader("File Upload")

code_column: DeltaGenerator
spec_column: DeltaGenerator

code_column, spec_column = st.columns([1, 1])
with code_column:
    st.markdown("Supported formats: `.txt`, `.abap`")
    code_files: List[UploadedFile] | None = st.file_uploader(
        label="Choose Code files",
        type=[".txt", ".abap"],  # Accept only .txt file types for ABAP code
        accept_multiple_files=True,  # Enable multiple file selection
        help="Select one or more files to upload",
    )
with spec_column:
    st.markdown("Supported formats: `.txt`, `.md`")
    spec_files: List[UploadedFile] | None = st.file_uploader(
        label="Choose Template files",
        type=[".txt", ".md"],  # Accept only .txt file types for ABAP code
        accept_multiple_files=True,  # Enable multiple file selection
        help="Select only one file to upload",
    )
# Visual separator between main content and documentation generation
st.markdown("---")
# File Upload Section - At the Top
st.subheader("File Path")

local_code_path_column: DeltaGenerator
local_spec_path_column: DeltaGenerator

local_code_path_column, local_spec_path_column = st.columns([1, 1])
with local_code_path_column:
    # Input field for local file path where code files are stored
    st.markdown("Local Code Files Path")
    local_code_path: str = st.text_input(
        key="id_code_files_path",  # Unique key for the input field
        label="Code Files Path",
        placeholder="Enter the file path for the code files",
        help="Provide the path where the code files are located",
        value=f"{getcwd()}\\document_generator\\code_files",  # Default to current working directory
    )
with local_spec_path_column:
    # Input field for local spec file path where template files are stored
    st.markdown("Local Spec File Path")
    local_spec_path: str = st.text_input(
        key="id_spec_file_path",  # Unique key for the input field
        label="Spec File Path",
        placeholder="Enter the file path for the spec file",
        help="Provide the path where the spec file is located",
        value=f"{getcwd()}\\document_generator\\templates",  # Default to current working directory
    )
st.markdown("---")
# Create columns for generate button (1:4 ratio for compact layout)
submit_button_column: DeltaGenerator
blank_column: DeltaGenerator
submit_button_column, blank_column = st.columns([1, 4])

with submit_button_column:
    # Primary action button for starting documentation generation
    if st.button(
        key="btn_submit",  # Unique key for the button
        label="Submit",
        disabled=False,  # Button is enabled when files are present
        use_container_width=True,  # Fill the column width
        help="Click to generate documentation for the uploaded files",
    ):
        if all([code_files, spec_files, local_code_path, local_spec_path]):
            processed_code_files: List[SchemaFile] = File_Processor_Streamlit.generate_code_file_list(
                code_file_list=code_files,
                code_file_path=local_code_path,
            )
            code_documents: List[Document] = TextDocumentLoader.load_text_documents(file_list=processed_code_files)

            processed_spec_files: List[SchemaFile] = File_Processor_Streamlit.generate_spec_file_list(
                spec_file_list=spec_files,
                spec_file_path=local_spec_path,
            )
            spec_documents: List[Document] = TextDocumentLoader.load_text_documents(file_list=processed_spec_files)
            prompt: Prompt = Prompt()
            prompt_text: str = prompt.get_prompt_technical_specification(
                code=code_documents,
                spec=spec_documents,
                mode="comprehensive",  # Use comprehensive mode for detailed documentation
            )
            # st.write(prompt_text)
            ollama: Llama3 = Llama3()
            if ollama.initialize_llm(model_name="OLLAMA"):
                # Placeholder for actual documentation generation logic
                # For now, we just simulate success
                st.success("Connected to Ollama server successfully.")
                with ollama.get_llm() as model:
                    # Generate documentation using the selected output format
                    result: BaseMessage = model.invoke(input=prompt_text)
                    st.write(result.content)  # Display the generated documentation content
            # Show success message when documentation generation is triggered
            st.success("Documentation generation started.")
        else:
            # Show error message when no files are uploaded
            st.error("Please upload code and template files first to generate documentation.")
