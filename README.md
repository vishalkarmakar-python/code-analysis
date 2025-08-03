# Python Development Environment Setup Guide

**Version: 2.5.0**

This comprehensive guide covers the complete setup of a Python development environment on Windows 11, including installation, configuration, tool setup, and essential workflows.

## Documentation Structure

This documentation is organized into separate guides for easy reference:

1. [VS Code Setup Guide](readme/vs-code-setup.md) - VS Code setup, Jupyter integration, and keyboard shortcuts
2. [Python Setup Guide](readme/python-setup.md) - Python installation and package management
3. [Git Setup Guide](readme/git-setup.md) - Git installation and essential commands
4. [Docker Setup Guide ](readme/docker-setup.md) - Docker setup with local Ollama with Open WebUI and Postgres with PGVector
5. [Code Formatting Guide](readme/code-formatting.md) - Setting up Black and Ruff for code formatting and linting
6. [Troubleshooting and Resources](readme/troubleshooting.md) - Common issues and additional learning resources
7. [ChatOllama](readme/chatOllama.md) - ChatOllama documentation from LangChain
8. [Tiktoken](readme/tiktoken.md) - TikToken documentation from Token Calculation

## Version History

| Version | Date       | Changes                                                                                                                                                    |
| ------- | ---------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 2.5.0   | 2025-03-28 | Reorganized package management and virtual environment sections, added Black/Ruff comparison, restructured Git commands, and updated configuration options |
| 2.4.0   | 2025-03-25 | Added comprehensive Jupyter Notebook setup and integration with VS Code                                                                                    |
| 2.3.9   | 2025-03-23 | Added UV and Poetry commands, improved formatting, added Python module execution method for UV                                                             |
| 2.3.0   | 2025-02-15 | Added VS Code configuration and keyboard shortcuts                                                                                                         |
| 2.2.0   | 2025-01-10 | Enhanced Git commands and troubleshooting section                                                                                                          |
| 2.1.0   | 2024-12-05 | Expanded virtual environment management                                                                                                                    |
| 2.0.0   | 2024-11-20 | Major restructuring and Python 3.12 compatibility                                                                                                          |
| 1.0.0   | 2024-10-15 | Initial setup guide                                                                                                                                        |

## Quick Start

For a new Python project setup, follow these steps:

1. **Install Python 3.12**: Follow the [Python Setup Guide](python-setup.md#standard-installation)
2. **Install VS Code**: Download from [code.visualstudio.com](https://code.visualstudio.com/)
3. **Install essential VS Code extensions**: See [VS Code Extensions](vscode-guide.md#essential-extensions)
4. **Set up Git**: Follow the [Git Setup Guide](git-setup.md#windows-installation)
5. **Create a new project**:

   ```bash
   # Create project directory and navigate to it
   mkdir my_project
   cd my_project

   # Initialize Git repository
   git init

   # Create virtual environment
   python -m venv .venv

   # Activate virtual environment
   .venv\Scripts\activate

   # Install essential packages
   pip install black ruff

   # Create project structure
   mkdir src tests docs
   ```

6. **Configure formatting tools**: See [Code Formatting Guide](code-formatting.md)

## Major Changes in Version 2.5.0

- **Reorganized Documentation**: Split into separate topic-specific files for easier navigation
- **Enhanced Package Management**: Expanded coverage of UV and Poetry tools
- **Black/Ruff Comparison**: Added detailed comparison of formatting/linting tools
- **Improved Git Commands**: Restructured Git commands by operation type for easier reference
- **Updated Configuration Options**: Added comprehensive configuration options for formatting tools

## Recommended Environment

This documentation is targeted for:

- Windows 11
- Python 3.12.2
- VS Code (Latest)
- Git 2.43.0 or newer

## Contributing

If you find errors or have suggestions for improvement, please open an issue or submit a pull request.
