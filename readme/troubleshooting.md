# Troubleshooting and Additional Resources

This guide covers common issues and solutions when working with Python development tools, as well as additional resources for further learning.

## Table of Contents

- [Troubleshooting](#troubleshooting)
  - [UV Command Not Recognized](#uv-command-not-recognized)
  - [Jupyter Notebook Troubleshooting](#jupyter-notebook-troubleshooting)
  - [General Troubleshooting](#general-troubleshooting)
- [Additional Resources](#additional-resources)

## Troubleshooting

### UV Command Not Recognized

If you encounter the error "The term 'uv' is not recognized..." when running UV commands:

1. **Use Python module execution**:

   ```bash
   python -m uv init
   python -m uv add package_name
   ```

   This method bypasses PATH environment issues by running UV through the Python interpreter directly.

2. **Find the executable location**:

   - Look in `C:\Program Files\Python312\Scripts\` (system-wide installation)
   - Or in `%USERPROFILE%\AppData\Roaming\Python\Python312\Scripts\` (user installation)
   - You can use the full path to the executable: `C:\path\to\uv.exe init`

3. **Add to PATH environment variable**:

   - Open "Edit the system environment variables" from Windows search
   - Click "Environment Variables"
   - Edit the "Path" variable and add the directory containing uv.exe
   - Restart your terminal or VS Code completely

4. **Reinstall with user flag**:
   ```bash
   pip install --user uv==0.1.24
   ```

### Jupyter Notebook Troubleshooting

| Problem                                  | Solution                                                       | Explanation                                         |
| ---------------------------------------- | -------------------------------------------------------------- | --------------------------------------------------- |
| Kernel not available                     | Run `python -m ipykernel install --user`                       | Installs the default kernel for the current Python  |
| Cannot find custom kernel                | Run `jupyter kernelspec list` to verify installation           | Confirms kernel is properly registered              |
| Kernel fails to start                    | Check `jupyter --paths` and verify permissions                 | Identifies configuration issues                     |
| "No module named X"                      | Run `pip install X` in the environment where kernel is running | The kernel uses the environment's packages          |
| Slow notebook performance                | Restart kernel and clear outputs                               | Frees memory and computational resources            |
| Notebook not saving changes              | Check disk space and permissions                               | Ensures file system is accessible                   |
| Kernel keeps disconnecting               | Check for resource limits or firewall issues                   | System constraints can cause kernel crashes         |
| Package not found in notebook            | Verify kernel is using the correct environment                 | Different kernels may use different environments    |
| Unable to import newly installed package | Restart kernel after installation                              | Kernel needs to refresh to see new packages         |
| VS Code can't find jupyter               | Run `pip install jupyter ipykernel notebook`                   | Ensures all required components are installed       |
| "kernel died" errors                     | Check environment conflicts or resource constraints            | Memory issues or package conflicts can kill kernels |
| Multiple kernels showing same env        | Run `jupyter kernelspec remove <old-kernel-name>`              | Cleans up kernel registry                           |
| Cannot access data in notebook           | Add parent directory to Python path using `sys.path.append()`  | Extends module search path in notebook              |
| VS Code extensions not activating        | Verify Jupyter extension is installed and enabled              | Extensions might need manual activation             |
| Plots not displaying                     | Try `%matplotlib inline` magic command                         | Forces inline plot rendering                        |
| Interactive widgets not working          | Run `pip install ipywidgets` and restart kernel                | Enables interactive components                      |

### General Troubleshooting

| Problem                             | Solution                                                           | Explanation                                                                 |
| ----------------------------------- | ------------------------------------------------------------------ | --------------------------------------------------------------------------- |
| "Permission denied" errors          | Run Command Prompt as Administrator                                | System directories require elevated privileges                              |
| Pip installs to user directory      | Use the `--target` flag                                            | Explicitly specifies the installation location                              |
| Environment variables not working   | Log out and log back in                                            | Some changes require session restart to take effect                         |
| Python not found in command line    | Verify PATH variable settings                                      | Ensures the system can find Python executables                              |
| Conflicts with existing Python      | Uninstall other versions first                                     | Removes potential interference from other installations                     |
| Poetry command not found            | Ensure `%APPDATA%\Python\Scripts` is in PATH                       | Poetry may install its executable here                                      |
| UV command not found                | Use `python -m uv` or reinstall with `pip install --user uv`       | Module execution bypasses PATH issues; reinstall ensures proper permissions |
| VS Code Jupyter extension error     | Run `pip install jupyter notebook ipykernel` in env                | Ensures all necessary components are installed                              |
| Multiple kernels showing same env   | Run `jupyter kernelspec remove <n>` for duplicates                 | Cleans up kernel registry                                                   |
| Black/Ruff not formatting           | Check VS Code settings.json and extensions                         | Ensure proper configuration and extension installation                      |
| Formatter conflicts                 | Don't enable both Black and Ruff for formatting                    | Choose one formatter to avoid conflicts                                     |
| pyproject.toml not recognized       | Place in project root directory                                    | File must be in the correct location to be found                            |
| Dependency conflicts                | Create fresh virtual environment                                   | Isolates packages to avoid version conflicts                                |
| Import errors after installation    | Restart VS Code or terminal                                        | Environment changes may require application restart                         |
| Git not recognizing credentials     | Run `git config --global credential.helper manager`                | Windows credential manager integration                                      |
| Module not found in virtual env     | Verify venv is activated, check pip install path                   | Virtual environments may not be properly activated                          |
| Package install fails with error    | Try `pip install --no-cache-dir <package>`                         | Bypasses potentially corrupted cache files                                  |
| Package doesn't match requirements  | Create fresh virtual env with confirmed requirements               | Ensures clean environment without package conflicts                         |
| VS Code Python extension not found  | Install from marketplace or extensions panel                       | VS Code extensions might need manual installation                           |
| VS Code not using the right Python  | Select interpreter via Command Palette: Python: Select Interpreter | VS Code might be using wrong Python version or environment                  |
| Linting/formatting rules conflict   | Configure one tool as primary in settings.json                     | Multiple tools may have conflicting rules                                   |
| Remote repo access denied           | Check credentials and SSH keys                                     | Authentication issues often prevent Git operations                          |
| "ValueError: source code not found" | Install tools in the right environment                             | VS Code might be looking in wrong environment for formatter/linter          |

## Additional Resources

These resources provide further information on tools, libraries, and best practices for Python development.

### Official Documentation

- [Python Official Documentation](https://docs.python.org/) - Python 3.12.2
- [VS Code Python Documentation](https://code.visualstudio.com/docs/languages/python) - Version 2023.22.0
- [Virtual Environment Documentation](https://docs.python.org/3/library/venv.html) - Python 3.12
- [Pip Documentation](https://pip.pypa.io/en/stable/) - Version 24.0
- [UV Documentation](https://github.com/astral-sh/uv) - Version 0.1.24
- [Poetry Documentation](https://python-poetry.org/docs/) - Version 1.7.1
- [Git Documentation](https://git-scm.com/doc) - Version 2.43.0
- [Jupyter Documentation](https://jupyter.org/documentation) - Current version
- [Black Documentation](https://black.readthedocs.io/en/stable/) - The uncompromising Python code formatter
- [Ruff Documentation](https://docs.astral.sh/ruff/) - An extremely fast Python linter and formatter

### Learning Resources

- [Real Python](https://realpython.com/) - Tutorials, guides, and articles on Python development
- [Python Bytes Podcast](https://pythonbytes.fm/) - Weekly Python news and updates
- [Talk Python to Me Podcast](https://talkpython.fm/) - In-depth interviews with Python developers
- [PyBites](https://pybit.es/) - Python challenges and learning resources
- [Awesome Python](https://github.com/vinta/awesome-python) - Curated list of Python resources
- [Python Morsels](https://www.pythonmorsels.com/) - Weekly Python exercises

### Tools and Extensions

- [IPython Documentation](https://ipython.readthedocs.io/en/stable/) - Core interactive computing
- [VS Code Jupyter Extension](https://marketplace.visualstudio.com/items?itemName=ms-toolsai.jupyter) - Official extension
- [Jupyter Keyboard Shortcuts](https://jupyter-notebook.readthedocs.io/en/stable/shortcuts.html) - Complete reference
- [PyLance Documentation](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance) - Language server with advanced type checking
- [Python Extension Pack](https://marketplace.visualstudio.com/items?itemName=donjayamanne.python-extension-pack) - Bundle of useful Python extensions for VS Code
- [GitLens](https://marketplace.visualstudio.com/items?itemName=eamodio.gitlens) - Git supercharged for VS Code
- [Git Graph](https://marketplace.visualstudio.com/items?itemName=mhutchie.git-graph) - View Git history graphically
