# ABAP Code Analysis with AI

This project is a Python application that leverages large language models (LLMs) to analyze ABAP (Advanced Business Application Programming) code. It automatically loads ABAP source code files, splits them into manageable chunks, analyzes each chunk for its logic and purpose, and generates a comprehensive report in Markdown format.

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
- [Ollama](https://ollama.ai/) installed and running with a desired language model (e.g., `qwen:7b-chat`).

## Installation

1.  **Clone the repository:**

    ```bash
    git clone [https://github.com/your-username/abap-code-analysis.git](https://github.com/your-username/abap-code-analysis.git)
    cd abap-code-analysis
    ```

2.  **Create a virtual environment:**

    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
    ```

3.  **Install the dependencies:**

    ```bash
    pip install -r requirements.txt
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
