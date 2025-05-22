# Langchain Components for Ollama + Llama 3.2 3b ABAP Analyzer

This document outlines the essential Langchain components required for building a Python application that:

1. Takes an ABAP code file as input
2. Analyzes the code using Llama 3.2 3b via Ollama running in Docker
3. Generates a technical specification document in markdown, PDF, or DOCX format

## Core Langchain Packages

| Package                    | Description                                                    |
| -------------------------- | -------------------------------------------------------------- |
| `langchain`                | Core package containing chains and other high-level components |
| `langchain-core`           | Core abstractions and base classes                             |
| `langchain-community`      | Community-contributed integrations for APIs like Ollama        |
| `langchain-text-splitters` | Text splitting utilities for processing ABAP code files        |

## Document Processing

| Component                        | Class                                                               | Description                                         |
| -------------------------------- | ------------------------------------------------------------------- | --------------------------------------------------- |
| `TextLoader`                     | `langchain_community.document_loaders.text.TextLoader`              | Loads ABAP code from .txt files                     |
| `RecursiveCharacterTextSplitter` | `langchain_text_splitters.character.RecursiveCharacterTextSplitter` | Splits large ABAP code files into manageable chunks |
| `Document`                       | `langchain_core.documents.Document`                                 | Container for text chunks and metadata              |

## LLM Integration

| Component       | Class                                                      | Description                                |
| --------------- | ---------------------------------------------------------- | ------------------------------------------ |
| `ChatOllama`    | `langchain_community.chat_models.ollama.ChatOllama`        | Connect to Ollama API for chat completions |
| `Ollama`        | `langchain_community.llms.ollama.Ollama`                   | Connect to Ollama API for text completions |
| `BaseChatModel` | `langchain_core.language_models.chat_models.BaseChatModel` | Base class for chat models                 |
| `BaseLLM`       | `langchain_core.language_models.llms.BaseLLM`              | Base class for language models             |

## Prompt Construction

| Component                     | Class                                                     | Description                  |
| ----------------------------- | --------------------------------------------------------- | ---------------------------- |
| `PromptTemplate`              | `langchain_core.prompts.prompt.PromptTemplate`            | Template for model prompts   |
| `ChatPromptTemplate`          | `langchain_core.prompts.chat.ChatPromptTemplate`          | Template for chat prompts    |
| `SystemMessagePromptTemplate` | `langchain_core.prompts.chat.SystemMessagePromptTemplate` | Template for system messages |
| `HumanMessagePromptTemplate`  | `langchain_core.prompts.chat.HumanMessagePromptTemplate`  | Template for human messages  |
| `MessagesPlaceholder`         | `langchain_core.prompts.chat.MessagesPlaceholder`         | Placeholder for messages     |

## Ollama Configuration

| Component     | Parameter                | Description                                                  |
| ------------- | ------------------------ | ------------------------------------------------------------ |
| `base_url`    | `http://localhost:11434` | Ollama API endpoint                                          |
| `model`       | `llama3:3b`              | Llama 3.2 3b model name in Ollama                            |
| `temperature` | `0.0 - 1.0`              | Controls randomness (lower for more deterministic responses) |
| `num_ctx`     | `2048 - 8192`            | Context window size for processing text                      |
| `num_predict` | Integer                  | Maximum number of tokens to generate                         |
| `top_p`       | `0.0 - 1.0`              | Nucleus sampling parameter                                   |
| `top_k`       | Integer                  | Top-k sampling parameter                                     |
| `stop`        | List[str]                | Sequences that trigger the end of generation                 |

## Chains and Response Processing

| Component              | Class/Method                                                      | Description                                 |
| ---------------------- | ----------------------------------------------------------------- | ------------------------------------------- |
| `LLMChain`             | `langchain.chains.llm.LLMChain`                                   | Chain for connecting prompts to LLM         |
| `SequentialChain`      | `langchain.chains.sequential.SequentialChain`                     | Chain for sequential operations             |
| `LCEL`                 | `langchain.chains.combine_documents.create_stuff_documents_chain` | LangChain Expression Language for pipelines |
| `RunnablePassthrough`  | `langchain_core.runnables.passthrough.RunnablePassthrough`        | Passes inputs through a chain               |
| `StrOutputParser`      | `langchain_core.output_parsers.string.StrOutputParser`            | Parses output as string                     |
| `PydanticOutputParser` | `langchain_core.output_parsers.pydantic.PydanticOutputParser`     | Parses output into Pydantic models          |

## Output Format Handling

| Component     | Class/Module         | Description                               |
| ------------- | -------------------- | ----------------------------------------- |
| `pypdf`       | `pypdf.PdfWriter`    | Creates PDF files from generated content  |
| `python-docx` | `docx.Document`      | Creates DOCX files from generated content |
| `markdown`    | Direct string output | Native markdown format output             |

## ABAP-Specific Analysis Components

| Component                                                              | Description                                           |
| ---------------------------------------------------------------------- | ----------------------------------------------------- |
| `create_extraction_chain`                                              | Extraction of ABAP structures, functions, and methods |
| `Language.ABAP`                                                        | ABAP language enum for CodeTextSplitter               |
| `RecursiveCharacterTextSplitter.from_language(language=Language.ABAP)` | ABAP-specific text splitter                           |

## File System Operations

| Component      | Method                            | Description                            |
| -------------- | --------------------------------- | -------------------------------------- |
| `os.path`      | Path handling                     | For managing input/output file paths   |
| `pathlib.Path` | Object-oriented path manipulation | Modern path handling                   |
| `open()`       | File I/O                          | Reading input and writing output files |

## Structured Output with Pydantic

| Component   | Class                | Description                        |
| ----------- | -------------------- | ---------------------------------- |
| `BaseModel` | `pydantic.BaseModel` | Base class for data models         |
| `Field`     | `pydantic.Field`     | Field with metadata for validation |
| `validator` | `pydantic.validator` | Custom validation methods          |

## Example Output Models

```python
from pydantic import BaseModel, Field
from typing import List, Dict, Optional

class AbapFunction(BaseModel):
    """Represents an ABAP function module"""
    name: str = Field(description="Name of the function module")
    description: str = Field(description="Purpose of the function")
    parameters: List[Dict[str, str]] = Field(description="Input/output parameters")
    source_code: Optional[str] = Field(None, description="Function source code")

class AbapClass(BaseModel):
    """Represents an ABAP class"""
    name: str = Field(description="Name of the class")
    description: str = Field(description="Purpose of the class")
    methods: List[Dict[str, str]] = Field(description="Class methods")
    attributes: List[Dict[str, str]] = Field(description="Class attributes")

class AbapTechnicalSpec(BaseModel):
    """Technical specification for ABAP code"""
    title: str = Field(description="Document title")
    overview: str = Field(description="Overall code description")
    functions: List[AbapFunction] = Field(description="Function modules found")
    classes: List[AbapClass] = Field(description="Classes found")
    database_tables: List[str] = Field(description="Database tables used")
    recommendations: List[str] = Field(description="Code improvement suggestions")
```

## Sample Ollama Chain Implementation

```python
from langchain_community.llms.ollama import Ollama
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain

# Initialize Ollama with the local endpoint
llm = Ollama(
    model="llama3:3b",
    base_url="http://localhost:11434",
    temperature=0.1
)

# Create a template for ABAP analysis
template = """
You are an expert ABAP developer and technical writer.
Analyze the following ABAP code and create a detailed technical description:

{abap_code}

Focus on identifying:
1. Functions and their purpose
2. Classes and methods
3. Database tables used
4. Overall program structure
5. Recommendations for improvement

Output in a well-structured markdown format.
"""

prompt = PromptTemplate(
    input_variables=["abap_code"],
    template=template
)

# Create the chain
abap_analysis_chain = LLMChain(
    llm=llm,
    prompt=prompt,
    output_key="technical_spec"
)
```

## Utility Functions

| Function                                            | Purpose                        |
| --------------------------------------------------- | ------------------------------ |
| `convert_markdown_to_pdf(md_content, output_path)`  | Converts markdown to PDF       |
| `convert_markdown_to_docx(md_content, output_path)` | Converts markdown to DOCX      |
| `extract_abap_structures(code)`                     | Extracts key ABAP structures   |
| `split_abap_code(code)`                             | Splits ABAP code intelligently |
| `analyze_code_quality(code)`                        | Assesses code quality metrics  |

## Command Line Interface

```python
import argparse

parser = argparse.ArgumentParser(description='ABAP Code Analyzer')
parser.add_argument('input_file', help='Path to ABAP code .txt file')
parser.add_argument(
    '--format',
    choices=['md', 'pdf', 'docx'],
    default='md',
    help='Output format (default: md)'
)
parser.add_argument(
    '--output',
    help='Output file path (optional)'
)
```

## Docker Configuration

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Command to run the application
ENTRYPOINT ["python", "abap_analyzer.py"]
```

## Required Dependencies in requirements.txt

```plaintext
langchain>=0.1.0
langchain-community>=0.0.13
langchain-core>=0.1.17
langchain-text-splitters>=0.0.1
pydantic>=2.5.2
pypdf>=3.17.1
python-docx>=1.0.1
markdown>=3.4.4
mdpdf>=0.0.17
requests>=2.31.0
argparse>=1.4.0
```
