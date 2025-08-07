# Python Installation and Package Management Guide

This guide provides detailed instructions for installing Python on Windows 11 and managing packages using various tools such as pip, UV, and Poetry.

## Table of Contents

- [Python Installation](#python-installation)
  - [Standard Installation](#standard-installation)
  - [Custom Installation Steps](#custom-installation-steps)
  - [Configuration Files](#configuration-files)
  - [Environment Variables](#environment-variables)
  - [Manually Setting Environment Variables](#manually-setting-environment-variables)
  - [Verification Steps](#verification-steps)
- [Package Management and Virtual Environment](#package-management-and-virtual-environment)
  - [Pip Commands](#pip-commands)
  - [UV Commands](#uv-commands)
  - [Poetry Commands](#poetry-commands)

## Python Installation

This section provides detailed instructions for installing Python on Windows 11 using either the standard installation method or a custom approach that stores all components in `C:\Program Files\Python`.

### Standard Installation

A standard Python installation is the simplest approach and suitable for most users, especially beginners. This method installs Python in the user's profile and handles most configuration automatically.

| Step | Description                | Details                                                                                  |
| ---- | -------------------------- | ---------------------------------------------------------------------------------------- |
| 1    | Download installer         | Visit https://www.python.org/downloads/windows/ and download the latest 64-bit installer |
| 2    | Run installer              | Double-click the downloaded file (no admin privileges required)                          |
| 3    | Check "Add Python to PATH" | Important! This makes Python available from command line                                 |
| 4    | Click "Install Now"        | Uses default installation settings                                                       |
| 5    | Wait for installation      | Installer will show progress bar                                                         |
| 6    | Click "Close"              | Installation complete                                                                    |

#### Default Paths for Standard Installation

When using standard installation, Python creates several important directories:

| Path Type          | Typical Location                                                                 | Purpose                                             |
| ------------------ | -------------------------------------------------------------------------------- | --------------------------------------------------- |
| Main installation  | `C:\Users\{username}\AppData\Local\Programs\Python\Python312\`                   | Python executable and standard library              |
| Scripts directory  | `C:\Users\{username}\AppData\Local\Programs\Python\Python312\Scripts\`           | Command-line tools and executables installed by pip |
| Site-packages      | `C:\Users\{username}\AppData\Local\Programs\Python\Python312\Lib\site-packages\` | Third-party packages installed by pip               |
| User site-packages | `C:\Users\{username}\AppData\Roaming\Python\Python312\site-packages\`            | Packages installed with `pip install --user`        |
| User scripts       | `C:\Users\{username}\AppData\Roaming\Python\Python312\Scripts\`                  | Scripts from packages installed with `--user` flag  |
| pip.ini (user)     | `C:\Users\{username}\AppData\Roaming\pip\pip.ini`                                | User-specific pip configuration                     |

Understanding these locations is important for troubleshooting and advanced configuration. For most users, these paths are automatically managed by Python and pip.

### Custom Installation Steps

For system administrators or users requiring a system-wide installation, the following steps install Python in `C:\Program Files\Python` instead of user-specific locations.

1. **Download the Official Python Installer**

   - Visit https://www.python.org/downloads/windows/
   - Download the 64-bit executable installer (.exe) for Python 3.12.x (current version: 3.12.2)

2. **Run the Installer with Administrative Privileges**

   - Right-click on the downloaded installer
   - Select "Run as administrator"
   - Confirm the UAC prompt

3. **Choose Custom Installation**

   - Uncheck "Add Python.exe to PATH" (we'll handle this manually)
   - Click on "Customize installation"

4. **Select Optional Features**

   - Ensure all features are selected
   - Click "Next"

5. **Configure Advanced Options**
   - Check "Install for all users" (critical)
   - Change installation location to `C:\Program Files\Python312` (or your preferred version)
   - Ensure "Add Python to environment variables" is checked
   - Click "Install"

### Configuration Files

#### sitecustomize.py

Create a file at `C:\Program Files\Python312\Lib\site-packages\sitecustomize.py`:

```python
import sys
import site

# Disable user site packages
site.ENABLE_USER_SITE = False

# Set preferred location
sys.prefix = r'C:\Program Files\Python312'
```

#### pip.ini

Create a file at `C:\Program Files\Python312\pip\pip.ini`:

```ini
[global]
no-user-cfg = true
target = C:\Program Files\Python312\Lib\site-packages
prefix = C:\Program Files\Python312

[install]
install-option = --prefix=C:\Program Files\Python312
no-user-cfg = true
no-warn-script-location = false
```

### Environment Variables

After installation, configure these system environment variables:

1. **PYTHONHOME**

   - **Value:** `C:\Program Files\Python312`

2. **PYTHONPATH**

   - **Value:** `C:\Program Files\Python312\Lib;C:\Program Files\Python312\Lib\site-packages`

3. **PATH** (append to existing)
   - Add `C:\Program Files\Python312`
   - Add `C:\Program Files\Python312\Scripts`

### Manually Setting Environment Variables

If environment variables were not created during installation or you need to modify them later, follow these steps:

#### Using GUI (Windows 11)

| Step | Description                | Details                                                           |
| ---- | -------------------------- | ----------------------------------------------------------------- |
| 1    | Open Settings              | Click Start → Settings or press Win+I                             |
| 2    | Navigate to System         | Click on "System" in Settings                                     |
| 3    | Open About                 | Scroll down and click "About"                                     |
| 4    | Open Advanced Settings     | Click "Advanced system settings"                                  |
| 5    | Open Environment Variables | Click "Environment Variables..." button                           |
| 6    | Add User Variable          | Click "New..." under "User variables" section                     |
| 7    | Add System Variable        | Click "New..." under "System variables" section (requires admin)  |
| 8    | Edit PATH                  | Select "Path" and click "Edit...", then "New" to add new entry    |
| 9    | Apply Changes              | Click "OK" on all dialog boxes                                    |
| 10   | Restart Applications       | Close and reopen Command Prompt/PowerShell and other applications |

#### Using Command Line (Administrator PowerShell)

For system-wide environment variables (requires administrator):

```powershell
# Set PYTHONHOME
[System.Environment]::SetEnvironmentVariable('PYTHONHOME', 'C:\Program Files\Python312', 'Machine')

# Set PYTHONPATH
[System.Environment]::SetEnvironmentVariable('PYTHONPATH', 'C:\Program Files\Python312\Lib;C:\Program Files\Python312\Lib\site-packages', 'Machine')

# Add to PATH (preserving existing entries)
$path = [System.Environment]::GetEnvironmentVariable('Path', 'Machine')
$newPath = $path + ';C:\Program Files\Python312;C:\Program Files\Python312\Scripts'
[System.Environment]::SetEnvironmentVariable('Path', $newPath, 'Machine')
```

For user-specific environment variables:

```powershell
# Set user-level environment variables
[System.Environment]::SetEnvironmentVariable('PYTHONHOME', 'C:\Program Files\Python312', 'User')
[System.Environment]::SetEnvironmentVariable('PYTHONPATH', 'C:\Program Files\Python312\Lib;C:\Program Files\Python312\Lib\site-packages', 'User')

# Add to user PATH
$path = [System.Environment]::GetEnvironmentVariable('Path', 'User')
$newPath = $path + ';C:\Program Files\Python312;C:\Program Files\Python312\Scripts'
[System.Environment]::SetEnvironmentVariable('Path', $newPath, 'User')
```

#### Testing Environment Variables

After setting environment variables, open a new command prompt and verify:

```cmd
echo %PYTHONHOME%
echo %PYTHONPATH%
echo %PATH%
where python
python --version
```

If environment variables are correctly set, these commands should display the expected values and Python should be found at the specified location.

### Verification Steps

To verify proper installation:

```cmd
python -c "import sys; print(sys.prefix)"
python -c "import site; print(site.getsitepackages())"
python -c "import site; print(site.ENABLE_USER_SITE)"
```

## Package Management and Virtual Environment

This section covers package management and virtual environment commands for pip, UV, and Poetry, organized by workflow.

### Pip Commands

| Operation                        | Command                                                    | Description                                                 |
| -------------------------------- | ---------------------------------------------------------- | ----------------------------------------------------------- |
| **Installation**                 |                                                            |                                                             |
| Install pip (latest)             | `python -m ensurepip --upgrade`                            | Ensure pip is installed and updated                         |
| Update pip                       | `python -m pip install --upgrade pip`                      | Update to latest pip version                                |
| **Project Setup**                |                                                            |                                                             |
| Create virtual environment       | `python -m venv .venv`                                     | Create virtual environment in current directory             |
| Activate virtual env (Windows)   | `.venv\Scripts\activate`                                   | Activate the environment on Windows                         |
| Activate virtual env (Unix)      | `source .venv/bin/activate`                                | Activate the environment on macOS/Linux                     |
| Deactivate virtual environment   | `deactivate`                                               | Exit the virtual environment                                |
| **Package Management**           |                                                            |                                                             |
| Install package                  | `pip install package_name`                                 | Install the latest version of a package                     |
| Install specific version         | `pip install package_name==1.2.3`                          | Install exact version of a package                          |
| Install with constraints         | `pip install "package_name>=1.0.0,<2.0.0"`                 | Install with version range constraints                      |
| Install from requirements        | `pip install -r requirements.txt`                          | Install all packages listed in requirements file            |
| Install development dependencies | `pip install -e ".[dev]"`                                  | Install package in development mode with extra dependencies |
| Install to specific location     | `pip install --target="C:\path\to\directory" package_name` | Install to a custom directory                               |
| **Updating Packages**            |                                                            |                                                             |
| Update package                   | `pip install --upgrade package_name`                       | Update an existing package to latest version                |
| Update all packages              | `pip install --upgrade $(pip freeze \| cut -d= -f1)`       | Update all installed packages (Unix)                        |
| **Managing Requirements**        |                                                            |                                                             |
| Generate requirements            | `pip freeze > requirements.txt`                            | Create requirements file from installed packages            |
| Check outdated packages          | `pip list --outdated`                                      | Show packages with available updates                        |
| **Other Commands**               |                                                            |                                                             |
| Uninstall package                | `pip uninstall package_name`                               | Remove an installed package                                 |
| Show package info                | `pip show package_name`                                    | Display metadata for a specific package                     |
| List installed packages          | `pip list`                                                 | Show all installed packages                                 |
| Check package dependencies       | `pip show -f package_name`                                 | Show files and dependencies for a package                   |
| Verify dependencies              | `pip check`                                                | Verify installed packages have compatible dependencies      |

### UV Commands

UV is a fast Python package installer and resolver.

| Operation                      | Command                                                    | Alternative (if UV not in PATH)                                      | Description                                         |
| ------------------------------ | ---------------------------------------------------------- | -------------------------------------------------------------------- | --------------------------------------------------- |
| **Installation**               |                                                            |                                                                      |                                                     |
| Install UV                     | `pip install uv==0.1.24`                                   | -                                                                    | Install UV package manager (current stable version) |
| Verify installation            | `uv --version`                                             | `python -m uv --version`                                             | Check UV installation                               |
| **Project Setup**              |                                                            |                                                                      |                                                     |
| Initialize project             | `uv init`                                                  | `python -m uv init`                                                  | Create a new project configuration                  |
| Initialize project with name   | `uv init<project_name> --description<project_description>` | `python -m uv init<project_name> --description<project_description>` | Create a new project with name and description      |
| Create virtual environment     | `uv venv`                                                  | `python -m uv venv`                                                  | Create a new virtual environment                    |
| Create with specific Python    | `uv venv --python=3.11`                                    | `python -m uv venv --python=3.11`                                    | Create with specific Python version                 |
| Activate virtual env (Windows) | `.venv\Scripts\activate`                                   | -                                                                    | Activate the environment on Windows                 |
| Activate virtual env (Unix)    | `source .venv/bin/activate`                                | -                                                                    | Activate the environment on Unix systems            |
| Deactivate virtual environment | `deactivate`                                               | -                                                                    | Exit the virtual environment                        |
| **Package Management**         |                                                            |                                                                      |                                                     |
| Add package                    | `uv add package_name`                                      | `python -m uv add package_name`                                      | Add a package to your project                       |
| Add dev dependency             | `uv add --dev package_name`                                | `python -m uv add --dev package_name`                                | Add a development-only dependency                   |
| Add with version constraint    | `uv add "package_name>=1.0.0"`                             | `python -m uv add "package_name>=1.0.0"`                             | Add package with version constraints                |
| Install from requirements      | `uv pip sync requirements.txt`                             | `python -m uv pip sync requirements.txt`                             | Install packages from requirements file             |
| Install from pyproject.toml    | `uv sync`                                                  | `python -m uv sync`                                                  | Install dependencies from project file              |
| **Updating Packages**          |                                                            |                                                                      |                                                     |
| Update dependencies            | `uv pip sync --upgrade`                                    | `python -m uv pip sync --upgrade`                                    | Update all dependencies                             |
| Update specific package        | `uv add --upgrade package_name`                            | `python -m uv add --upgrade package_name`                            | Update a specific package                           |
| **Managing Requirements**      |                                                            |                                                                      |                                                     |
| Generate requirements          | `uv pip freeze > requirements.txt`                         | `python -m uv pip freeze > requirements.txt`                         | Create requirements file                            |
| **Package Analysis**           |                                                            |                                                                      |                                                     |
| View dependency tree           | `uv tree package_name`                                     | `python -m uv tree package_name`                                     | Display dependency tree for a specific package      |
| View all dependencies          | `uv tree`                                                  | `python -m uv tree`                                                  | Display entire dependency tree for project          |
| View with depth limit          | `uv tree --depth=2`                                        | `python -m uv tree --depth=2`                                        | Limit dependency tree depth to specified level      |
| **Other Commands**             |                                                            |                                                                      |                                                     |
| List packages                  | `uv pip list`                                              | `python -m uv pip list`                                              | List installed packages                             |
| Show outdated packages         | `uv pip list --outdated`                                   | `python -m uv pip list --outdated`                                   | Show packages with available updates                |
| Uninstall package              | `uv pip uninstall package_name`                            | `python -m uv pip uninstall package_name`                            | Remove an installed package                         |
| Show package info              | `uv pip show package_name`                                 | `python -m uv pip show package_name`                                 | Display package metadata                            |

### Poetry Commands

Poetry is a dependency management and packaging tool.

| Operation                    | Command                                                           | Description                                   |
| ---------------------------- | ----------------------------------------------------------------- | --------------------------------------------- |
| **Installation**             |                                                                   |                                               |
| Install Poetry               | `pip install poetry==1.7.1`                                       | Install Poetry tool (current stable version)  |
| Update Poetry                | `poetry self update`                                              | Update Poetry to latest version               |
| **Project Setup**            |                                                                   |                                               |
| Create new project           | `poetry new project-name`                                         | Create a new project with Poetry structure    |
| Initialize existing project  | `poetry init`                                                     | Add Poetry to an existing project             |
| Configure local envs         | `poetry config virtualenvs.in-project true`                       | Store environments in project directory       |
| Create and install           | `poetry install`                                                  | Create environment and install dependencies   |
| Activate shell               | `poetry shell`                                                    | Activate the poetry virtual environment       |
| Exit shell                   | `exit`                                                            | Exit poetry shell environment                 |
| **Package Management**       |                                                                   |                                               |
| Add dependency               | `poetry add package_name`                                         | Add a package dependency                      |
| Add dev dependency           | `poetry add --group dev package_name`                             | Add development-only dependency               |
| Add with version constraint  | `poetry add "package_name>=1.0.0"`                                | Add package with version constraints          |
| Install dependencies         | `poetry install`                                                  | Install all project dependencies              |
| Install production only      | `poetry install --without dev`                                    | Install without development dependencies      |
| **Updating Packages**        |                                                                   |                                               |
| Update all dependencies      | `poetry update`                                                   | Update all dependencies to latest versions    |
| Update specific package      | `poetry update package_name`                                      | Update a single package                       |
| **Managing Requirements**    |                                                                   |                                               |
| Show dependency tree         | `poetry show --tree`                                              | Display dependency relationships              |
| Export requirements          | `poetry export -f requirements.txt --output requirements.txt`     | Create standard requirements file             |
| Export with dev dependencies | `poetry export --with dev -f requirements.txt > requirements.txt` | Export including development dependencies     |
| **Building and Publishing**  |                                                                   |                                               |
| Build package                | `poetry build`                                                    | Build distributable package                   |
| Publish package              | `poetry publish`                                                  | Publish package to PyPI                       |
| Build and publish            | `poetry publish --build`                                          | Build and publish in one command              |
| **Other Commands**           |                                                                   |                                               |
| List packages                | `poetry show`                                                     | List all installed packages                   |
| Show outdated packages       | `poetry show --outdated`                                          | Show packages with available updates          |
| Show package info            | `poetry show package_name`                                        | Display detailed package information          |
| Check dependencies           | `poetry check`                                                    | Verify pyproject.toml validity                |
| Run script                   | `poetry run python script.py`                                     | Run script using poetry's virtual environment |
