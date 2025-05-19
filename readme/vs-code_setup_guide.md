# VS Code Setup Guide

This guide covers the complete setup of VS Code for Python development, including essential extensions, configurations, Jupyter Notebook integration, and keyboard shortcuts.

## Table of Contents

- [Essential Extensions](#essential-extensions)
- [Settings Configuration](#settings-configuration)
- [Jupyter Notebook Setup](#jupyter-notebook-setup)
  - [Installation Steps](#installation-steps)
  - [VS Code Integration](#vs-code-integration)
  - [Kernel Management](#kernel-management)
  - [Notebook Shortcuts](#notebook-shortcuts)
- [Keyboard Shortcuts](#keyboard-shortcuts)
  - [Terminal Shortcuts](#terminal-shortcuts)
  - [VS Code Shortcuts](#vs-code-shortcuts)
  - [Python Notebook Shortcuts](#python-notebook-shortcuts)

## Essential Extensions

1. **Python Extension** - Main Python support (v2023.22.0+)
2. **Black Formatter** - Code formatting (v2023.5.0+)
3. **Ruff** - Fast Python linter (v2023.11.0+)
4. **PyLint** - Code linting (v2023.10.1+)
5. **iSort** - Import organization (v2022.8.0+)
6. **Pylance** - Language server with advanced type checking (v2023.9.10+)
7. **Jupyter** - Enhanced Jupyter notebook support (v2023.3.1000+)

## Settings Configuration

Add the following to your VS Code workspace `settings.json`:

```json
{
  // Pylance settings
  "python.analysis.autoFormatStrings": true,
  "python.analysis.inlayHints.functionReturnTypes": true,
  "python.analysis.inlayHints.variableTypes": true,
  "python.analysis.inlayHints.callArgumentNames": "off",
  "python.languageServer": "Default",
  "python.analysis.typeCheckingMode": "standard",

  // Formatter settings
  "[python]": {
    "editor.defaultFormatter": "ms-python.black-formatter",
    "editor.wordWrapColumn": 200,
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
      "source.organizeImports": "always"
    }
  },

  // PyLint settings
  "pylint.args": [
    "W3101:missing-timeout" // Disable missing-timeout warning
  ],

  // iSort settings
  "isort.args": ["--profile", "black"],

  // Jupyter settings
  "jupyter.askForKernelRestart": false,
  "jupyter.codeLenses": "all",
  "jupyter.themeMatplotlibPlots": true,
  "jupyter.enableExtendedKernelCompletions": true
}
```

## Jupyter Notebook Setup

### Installation Steps

| Step | Description                                    | Command                                                                                                                                          |
| ---- | ---------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| 1    | Create virtual environment in project          | `python -m venv .venv`                                                                                                                           |
| 2    | Activate the virtual environment (Windows)     | `.\.venv\Scripts\activate`                                                                                                                       |
| 2a   | Activate the virtual environment (macOS/Linux) | `source .venv/bin/activate`                                                                                                                      |
| 3    | Install Jupyter core packages                  | `pip install ipykernel`                                                                                                                          |
| 4    | Create a project-specific kernel               | `python -m ipykernel install --prefix="C:\Users\<user_name>\<project_path>\.venv" --name=<project_name> --display-name="Kernel(<project_name>)"` |
| 5    | Install common data packages (optional)        | `pip install numpy pandas matplotlib seaborn scikit-learn`                                                                                       |

### VS Code Integration

| Setting            | Value                    | Description                                             |
| ------------------ | ------------------------ | ------------------------------------------------------- |
| Extension          | Jupyter                  | Required extension for notebook support                 |
| File Association   | `.ipynb`                 | VS Code automatically identifies Jupyter notebook files |
| Run Cell           | `Shift+Enter`            | Execute current cell and move to next                   |
| Run All            | Play button in toolbar   | Execute all cells in notebook                           |
| Variable Explorer  | Available in notebook UI | Inspect variable values during execution                |
| Kernel Selection   | Status bar               | Shows currently selected kernel                         |
| Interactive Window | Command Palette          | Alternative to notebooks for quick work                 |
| Plot Viewer        | Automatic                | Interactive plots display in output panel               |

### Kernel Management

| Operation              | Method                       | Details                                               |
| ---------------------- | ---------------------------- | ----------------------------------------------------- |
| Select Kernel          | Click "Select Kernel" button | Located in top-right of notebook                      |
| Change Kernel          | From command palette         | `Ctrl+Shift+P` then "Jupyter: Select Notebook Kernel" |
| Restart Kernel         | From notebook toolbar        | Click restart button or use command palette           |
| View Available Kernels | Command palette              | `Ctrl+Shift+P` then "Jupyter: Select Jupyter Server"  |
| Delete Custom Kernel   | Terminal command             | `jupyter kernelspec uninstall <kernel_name>`          |

## Keyboard Shortcuts

### Terminal Shortcuts

| Action                   | Shortcut            |
| ------------------------ | ------------------- |
| New integrated terminal  | `` Ctrl+Shift+`  `` |
| Open terminal            | `` Ctrl+`  ``       |
| Toggle terminal          | `` Ctrl+`  ``       |
| Close active terminal    | `Ctrl+Shift+W `     |
| Clear terminal           | `Ctrl+L`            |
| Navigate command history | `Up/Down Arrow`     |
| Interrupt command        | `Ctrl+C`            |
| Exit shell               | `Ctrl+D` or `exit`  |

### VS Code Shortcuts

| Action                    | Shortcut            | Description                              |
| ------------------------- | ------------------- | ---------------------------------------- |
| **Editor Navigation**     |                     |                                          |
| Format selection          | `Shift+F1`          | Format selected code                     |
| Format document           | `Shift+Alt+F`       | Format entire file                       |
| Go to line                | `Ctrl+G`            | Jump to specific line                    |
| Go to file                | `Ctrl+P`            | Quick file navigation                    |
| Go to symbol              | `Ctrl+Shift+O`      | Navigate to symbol in current file       |
| Go to definition          | `F12`               | Go to variable/function definition       |
| Find references           | `Shift+F12`         | Find all references to current selection |
| Quick info                | `Ctrl+K Ctrl+I`     | Show hover information                   |
| **Window Management**     |                     |                                          |
| Open integrated terminal  | `` Ctrl+Shift+`  `` | Open a new terminal                      |
| Close integrated terminal | `Ctrl+Shift+W`      | Close the current terminal               |
| Open new window           | `Ctrl+Shift+N`      | Create a new VS Code window              |
| Open new terminal         | `Ctrl+Shift+N`      | Create a new terminal                    |
| Split editor              | `Ctrl+\`            | Split editor vertically                  |
| Toggle sidebar visibility | `Ctrl+B`            | Show/hide sidebar                        |
| Toggle panel              | `Ctrl+J`            | Show/hide bottom panel                   |
| Window selection          | `Ctrl+Num`          | Switch between editor groups             |
| **Search and Replace**    |                     |                                          |
| Find in file              | `Ctrl+F`            | Search in current file                   |
| Replace in file           | `Ctrl+H`            | Replace in current file                  |
| Find in all files         | `Ctrl+Shift+F`      | Search across workspace                  |
| Replace in all files      | `Ctrl+Shift+H`      | Replace across workspace                 |
| **Other Functions**       |                     |                                          |
| Command palette           | `Ctrl+Shift+P`      | Execute VS Code commands                 |
| Markdown preview          | `Ctrl+K V`          | Preview Markdown file                    |
| Toggle comment            | `Ctrl+/`            | Comment/uncomment current line           |
| Fold code                 | `Ctrl+Shift+[`      | Fold current code block                  |
| Unfold code               | `Ctrl+Shift+]`      | Unfold current code block                |
| Rename symbol             | `F2`                | Rename variable/function                 |
| Show problems             | `Ctrl+Shift+M`      | Show problems panel                      |
| Quick fix                 | `Ctrl+.`            | Show code actions/quick fixes            |

### Python Notebook Shortcuts

| Action              | Shortcut                                        | Alternative Method                                      |
| ------------------- | ----------------------------------------------- | ------------------------------------------------------- |
| Create new notebook | Right-click in Explorer, "New Jupyter Notebook" | Command palette: "Jupyter: Create New Jupyter Notebook" |
| Add code cell       | Click "+" button in toolbar                     | Press "B" in command mode                               |
| Add markdown cell   | Click "+" then change type to Markdown          | Press "M" in command mode                               |
| Toggle cell output  | Double-click output section                     | No shortcut available                                   |
| Clear all outputs   | Command palette                                 | "Jupyter: Clear All Outputs"                            |
| Enter edit mode     | Click on cell or press Enter                    | Click inside cell content                               |
| Enter command mode  | Press Escape                                    | Click outside cell content                              |
| Run cell            | `Shift+Enter`                                   | Click run button in cell toolbar                        |
| Run all cells       | Command palette                                 | "Jupyter: Run All Cells"                                |
| Split cell          | `Ctrl+Shift+Minus`                              | Right-click menu: "Split Cell"                          |
| Merge cells         | `Shift+M` (in command mode)                     | Right-click menu: "Merge Cells"                         |
| Toggle line numbers | `L`                                             | In command mode                                         |
| Toggle output       | `O`                                             | In command mode                                         |
| Show keyboard help  | `H`                                             | In command mode                                         |
| Save notebook       | `Ctrl+S`                                        | Save current state                                      |
