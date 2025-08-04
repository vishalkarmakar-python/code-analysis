# ABAP Code Analysis with AI

This project is a Python application that leverages Ollama QWEN as LLM to analyze ABAP code. It automatically loads ABAP source code files, splits them into manageable chunks, analyzes each chunk for its logic and purpose, and generates a comprehensive analysis and summary in Markdown format.

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Workflow](#workflow)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Dependencies](#dependencies)
- [License](#license)

## Features

- **Automated Code Loading**: Recursively loads all `.abap` files from a specified directory.
- **Intelligent Code Splitting**: Splits large ABAP files into smaller, semantically coherent chunks.
- **AI-Powered Analysis**: Utilizes a local LLM via Ollama to analyze the functionality, logic, and purpose of each code chunk.
- **Structured Output**: Generates a structured analysis and summary for each code chunk.
- **Markdown Reports**: Creates detailed and easy-to-read Markdown reports for each analyzed file.

## Project Structure

```
    .
    ├── app
    │ ├── init.py
    │ ├── code_analysis.py
    │ ├── create_document.py
    │ ├── document_loader.py
    │ ├── document_splitter.py
    │ ├── language_model.py
    │ ├── prompt_generator.py
    │ └── structured_output.py
    ├── .env
    ├── .gitignore
    ├── pyproject.toml
    ├── README.md
    ├── requirements.txt
    └── run.py
```

## Workflow

1.  **Load Documents**: The application starts by loading all ABAP files from the user-provided directory.
2.  **Split Documents**: The loaded files are then split into smaller chunks, considering the code structure to maintain context.
3.  **Analyze Chunks**: Each chunk is individually sent to a large language model for analysis. The model provides a detailed explanation and a summary of the code.
4.  **Generate Report**: The analysis and summary for each chunk are compiled into a single Markdown file for each original ABAP file.

## Prerequisites

- Python 3.11 or higher
- Docker Desktop v4.40 or highr
- [Ollama](https://hub.docker.com/r/ollama/ollama) image installed in Docker Desktop.
- LLM: [qwen2.5-coder:7b](https://ollama.com/library/qwen2.5-coder:7b) for analyzing ABAP Code.

## Installation

1. **VS Code**

   - Install [VS-Code](https://code.visualstudio.com/)

2. **Python**

   - Download [Python](https://www.python.org/downloads/)

3. **UV**

   - Project Management tool for [Python](https://docs.astral.sh/uv/guides/install-python/#getting-started)

4. **RUFF**

   - Linter for [Python](https://docs.astral.sh/ruff/installation/)

5. **Clone the repository:**
   [code-analysis](https://github.com/vishalkarmakar-python/code-analysis.git)

   ```bash
   git clone https://github.com/vishalkarmakar-python/code-analysis.git
   cd code-analysis
   ```

6. **Create a virtual environment:**

   - `uv venv .venv`
   - mac: `source .venv/bin/activate`
   - windows: `.venv\Scripts\activate`

7. **Install the dependencies:**

   ```bash
   uv add <library name>
   ```

## Configuration

1.  **Create a `.env` file** in the root directory of the project.
2.  **Add the following environment variables** to the `.env` file:

    ```env
    # LLM Configuration
    OLLAMA_MODEL_QWEN="qwen:7b-chat"
    OLLAMA_MODEL_BASE_URL="http://localhost:11434"
    OLLAMA_MODEL_TEMPERATURE=0.2

    # Database connection details (if needed)
    DATABASE_HOST="127.0.0.1"
    DATABASE_USER="postgres"
    DATABASE_PASSWORD="your_password"
    DATABASE_NAME="postgres"
    DATABASE_PORT="5432"
    ```

    Make sure the `OLLAMA_MODEL_QWEN` matches a model you have pulled with Ollama.

## Usage

1.  **Run the application:**

    ```bash
    python run.py
    ```

2.  **Provide the path** to the directory containing your ABAP source code files when prompted.

3.  The application will process the files and generate the analysis reports in the `analyzed_documents` directory.

## Dependencies

The main dependencies are listed in the `pyproject.toml` and `requirements.txt` files. Key libraries include:

- `langchain`
- `langchain-community`
- `langchain-ollama`
- `pydantic`
- `python-dotenv`

For a complete list of dependencies, please see the `requirements.txt` file.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
