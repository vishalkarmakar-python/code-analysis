# Code Formatting with Black and Ruff

This guide covers the setup and configuration of Black and Ruff, two powerful Python code formatting and linting tools.

## Table of Contents

- [Installation Methods](#installation-methods)
- [Black vs Ruff Comparison](#black-vs-ruff-comparison)
- [Configuration Options](#configuration-options)
  - [Configuration Files](#configuration-files)
  - [VS Code Settings](#vs-code-settings)
  - [Configuration Parameters](#configuration-parameters)

## Installation Methods

| Tool  | Via Pip             | Via UV         | VS Code Extension                                                  |
| ----- | ------------------- | -------------- | ------------------------------------------------------------------ |
| Black | `pip install black` | `uv add black` | Search "Black Formatter" in Extensions (ms-python.black-formatter) |
| Ruff  | `pip install ruff`  | `uv add ruff`  | Search "Ruff" in Extensions (charliermarsh.ruff)                   |

## Black vs Ruff Comparison

| Feature                | Black                                 | Ruff                                            |
| ---------------------- | ------------------------------------- | ----------------------------------------------- |
| Primary Purpose        | Code formatter                        | Linter with formatting capabilities             |
| Speed                  | Fast                                  | Very fast (Rust-based implementation)           |
| Customization          | Limited (opinionated formatter)       | Highly customizable                             |
| Configuration Files    | pyproject.toml                        | pyproject.toml or ruff.toml                     |
| Line Length Default    | 88 characters                         | 88 characters (matches Black)                   |
| Import Sorting         | No (requires isort)                   | Yes (built-in)                                  |
| Style Fixes            | Formatting only                       | Formatting + many lint fixes                    |
| Code Complexity Checks | No                                    | Yes                                             |
| Type Checking          | No                                    | No (use mypy or Pylance)                        |
| Compatibility          | Works with most Python versions       | Python 3.7+                                     |
| VS Code Integration    | Via extension                         | Via extension                                   |
| Key Benefit            | Consistency, no arguments about style | Speed, combines multiple tools in one           |
| Limitations            | No linting, only formatting           | Newer tool with occasional compatibility issues |

## Configuration Options

### Configuration Files

| File Location           | Purpose                                        | Scope                             |
| ----------------------- | ---------------------------------------------- | --------------------------------- |
| VS Code settings.json   | Configure VS Code behavior and extensions      | User-wide or workspace settings   |
| Workspace settings.json | Project-specific VS Code settings              | Applied only to current workspace |
| pyproject.toml          | Tool configuration in standard Python projects | Project-specific settings         |
| ruff.toml               | Dedicated Ruff configuration file              | Project-specific Ruff settings    |

### VS Code Settings

#### settings.json (User Settings)

```json
{
  // Black settings
  "python.formatting.provider": "black",
  "python.formatting.blackArgs": [
    "--line-length",
    "88",
    "--target-version",
    "py310"
  ],
  "[python]": {
    "editor.defaultFormatter": "ms-python.black-formatter",
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
      "source.organizeImports": "always",
      "source.fixAll.ruff": "explicit",
      "source.organizeImports.ruff": "explicit"
    }
  },
  "black-formatter.args": ["--line-length", "88"],

  // Ruff settings
  "ruff.enable": true,
  "ruff.organizeImports": true,
  "ruff.fixAll": true,
  "ruff.format": false
}
```

| Setting                       | Description                                    | Default Value |
| ----------------------------- | ---------------------------------------------- | ------------- |
| `python.formatting.provider`  | Specifies which formatter to use               | "none"        |
| `python.formatting.blackArgs` | Arguments to pass to Black                     | []            |
| `editor.defaultFormatter`     | Formatter to use for Python files              | null          |
| `editor.formatOnSave`         | Whether to format when saving                  | false         |
| `editor.codeActionsOnSave`    | Actions to run on save                         | {}            |
| `black-formatter.args`        | Arguments for the Black extension              | []            |
| `ruff.enable`                 | Enable/disable Ruff linter                     | true          |
| `ruff.organizeImports`        | Use Ruff to organize imports                   | false         |
| `ruff.fixAll`                 | Apply all Ruff auto-fixes                      | false         |
| `ruff.format`                 | Use Ruff as formatter (conflicting with Black) | false         |

#### workspace.json (Workspace Settings)

```json
{
  // Path settings - specific to this workspace
  "python.formatting.blackPath": "${workspaceFolder}/.venv/Scripts/black",
  "black-formatter.path": ["${workspaceFolder}/.venv/Scripts/black"],
  "ruff.path": ["${workspaceFolder}/.venv/Scripts/ruff"]
}
```

| Setting                       | Description                     | Use Case                                  |
| ----------------------------- | ------------------------------- | ----------------------------------------- |
| `python.formatting.blackPath` | Path to Black executable        | Use virtual env's Black instead of global |
| `black-formatter.path`        | Path to Black for the extension | Same as above, but for the extension      |
| `ruff.path`                   | Path to Ruff executable         | Use virtual env's Ruff instead of global  |

### Configuration Parameters

#### pyproject.toml

```toml
[tool.black]
line-length = 88
target-version = ['py310']
include = '\.pyi?$'
exclude = '''
/(
    \.git
  | \.hg
  | \.mypy_cache
  | \.tox
  | \.venv
  | _build
  | buck-out
  | build
  | dist
)/
'''

[tool.ruff]
# Enable flake8-bugbear (`B`) rules.
select = ["E", "F", "B", "I"]
ignore = ["E501"]  # Line length handled by Black

# Same as Black.
line-length = 88
indent-width = 4

# Assume Python 3.10
target-version = "py310"

# Allow imports relative to the "src" and "app" directories.
src = ["src", "app", "tests"]

[tool.ruff.format]
# Use double quotes for strings.
quote-style = "double"

# Indent with spaces, rather than tabs.
indent-style = "space"

# Respect line length defined above
line-ending = "auto"

[tool.ruff.lint.isort]
known-first-party = ["my_package"]
known-third-party = ["numpy", "pandas", "pytest"]
```

#### ruff.toml

When you prefer a dedicated configuration file for Ruff instead of including settings in `pyproject.toml`, you can use `ruff.toml`:

```toml
# Enable flake8-bugbear (`B`) rules
select = ["E", "F", "B", "I"]
ignore = ["E501"]  # Line length handled by Black

# Same as Black
line-length = 88
indent-width = 4

# Assume Python 3.10
target-version = "py310"

# Allow imports relative to the "src" and "app" directories
src = ["src", "app", "tests"]

# Exclude files and directories from linting
exclude = [
    ".git",
    ".github",
    ".pytest_cache",
    ".ruff_cache",
    ".venv",
    "__pypackages__",
    "build",
    "dist",
    "venv",
]

# Per-file ignores
[per-file-ignores]
"__init__.py" = ["F401"]  # Unused imports
"test_*.py" = ["E501"]    # Line too long in test files

# Formatting configuration
[format]
quote-style = "double"
indent-style = "space"
line-ending = "auto"
docstring-code-format = true

# Import sorting configuration
[lint.isort]
known-first-party = ["my_package"]
known-third-party = ["numpy", "pandas", "pytest"]
required-imports = ["from __future__ import annotations"]

# Ruff-specific settings
[lint]
explicit-string-type = true
pydocstyle = { convention = "google" }
flake8-quotes = { style = "double" }
pylint = { max-args = 8 }
```

## Common Rule Sets in Ruff

| Rule Prefix | Name                  | Description                                       |
| ----------- | --------------------- | ------------------------------------------------- |
| `E`, `W`    | pycodestyle           | PEP 8 style guide enforcement                     |
| `F`         | Pyflakes              | Passive Python checker for logical errors         |
| `B`         | flake8-bugbear        | Catches common bugs and design problems           |
| `I`         | isort                 | Import sorting and organization                   |
| `C`         | flake8-comprehensions | Better list/dict/set comprehensions               |
| `N`         | pep8-naming           | PEP 8 naming conventions                          |
| `D`         | pydocstyle            | Docstring style checker                           |
| `UP`        | pyupgrade             | Automatically upgrade Python syntax               |
| `ANN`       | flake8-annotations    | Type annotation checks                            |
| `S`         | flake8-bandit         | Security-focused lints                            |
| `A`         | flake8-builtins       | Check for shadowed built-in names                 |
| `COM`       | flake8-commas         | Enforces trailing commas                          |
| `SIM`       | flake8-simplify       | Simplifies code where possible                    |
| `T10`       | flake8-debugger       | Check for debugger imports and calls              |
| `ERA`       | eradicate             | Find commented-out code                           |
| `PL`        | Pylint                | General Python linting rules                      |
| `RUF`       | Ruff-specific rules   | Rules specific to the Ruff linter                 |
| `TRY`       | tryceratops           | Improves exception handling and try/except blocks |
| `FLY`       | flynt                 | String formatting lints                           |
| `PERF`      | Perflint              | Performance-focused lints                         |

## Detailed Explanation of Ruff Configuration Parameters

### Root Configuration Parameters

| Parameter            | Description                               | Possible Values                                                                | Meaning                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| -------------------- | ----------------------------------------- | ------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `select`             | Rule codes to enable                      | Array of strings like `["E", "F", "B", "I"]`                                   | Each letter/number corresponds to a rule group:<br>- `E`: pycodestyle errors<br>- `F`: Pyflakes rules<br>- `B`: flake8-bugbear rules<br>- `I`: isort rules<br>- `C`: flake8-comprehensions<br>- `N`: pep8-naming<br>- `D`: pydocstyle<br>- `UP`: pyupgrade<br>- `ANN`: flake8-annotations<br>- `S`: flake8-bandit (security)<br>- `BLE`: flake8-blind-except<br>- `A`: flake8-builtins<br>- `COM`: flake8-commas<br>- `C4`: flake8-comprehensions<br>- `DTZ`: flake8-datetimez<br>- `T10`: flake8-debugger<br>- `EM`: flake8-errmsg<br>- `EXE`: flake8-executable<br>- `ISC`: flake8-implicit-str-concat<br>- `ICN`: flake8-import-conventions<br>- `G`: flake8-logging-format<br>- `INP`: flake8-no-pep420<br>- `PIE`: flake8-pie<br>- `T20`: flake8-print<br>- `PYI`: flake8-pyi<br>- `PT`: flake8-pytest-style<br>- `Q`: flake8-quotes<br>- `RSE`: flake8-raise<br>- `RET`: flake8-return<br>- `SLF`: flake8-self<br>- `SLOT`: flake8-slots<br>- `SIM`: flake8-simplify<br>- `TID`: flake8-tidy-imports<br>- `TCH`: flake8-type-checking<br>- `INT`: flake8-gettext<br>- `ARG`: flake8-unused-arguments<br>- `PTH`: flake8-use-pathlib<br>- `TD`: flake8-todos<br>- `FIX`: flake8-fixme<br>- `ERA`: eradicate<br>- `PD`: pandas-vet<br>- `PGH`: pygrep-hooks<br>- `PL`: Pylint<br>- `TRY`: tryceratops<br>- `FLY`: flynt<br>- `PERF`: Perflint<br>- `RUF`: Ruff-specific rules |
| `ignore`             | Rule codes to ignore globally             | Array of strings like `["E501", "F401"]`                                       | Specific rule codes to ignore. Can be broad (like `"E"` to ignore all pycodestyle errors) or specific (like `"E501"` to ignore line length errors)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| `line-length`        | Maximum line length                       | Integer (Default: 88 for Black compatibility)                                  | Maximum allowed length for lines in characters. Common values: 79 (PEP8), 88 (Black), 100 (Google style guide)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| `indent-width`       | Number of spaces per indentation level    | Integer (Default: 4)                                                           | Number of spaces to use for each level of indentation. Common values: 2, 4, 8                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| `target-version`     | Python version to target                  | String: `"py37"`, `"py38"`, `"py39"`, `"py310"`, `"py311"`, `"py312"`          | Determines language features available and version-specific rules. Should match the minimum supported Python version for your project                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| `src`                | Directories to be considered as source    | Array of strings like `["src", "app", "tests"]`                                | Directories that should be treated as source code, enabling relative imports between these directories                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| `exclude`            | Files/directories to exclude from linting | Array of strings, typically glob patterns like `[".git", "**/*.pyc", "build"]` | Files or directories to completely exclude from linting. Uses glob pattern matching                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| `extend-exclude`     | Additional exclusions                     | Array of strings                                                               | Additional patterns to exclude, without replacing the default exclusions                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| `external`           | External tool configs to respect          | Array of strings like `["black", "isort"]`                                     | Ruff will attempt to read configuration from these external tools                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| `extend-select`      | Additional rules to enable                | Array of rule codes                                                            | Rules to enable in addition to those in `select`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| `extend-ignore`      | Additional rules to ignore                | Array of rule codes                                                            | Rules to ignore in addition to those in `ignore`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| `fix`                | Whether to auto-fix violations            | Boolean: `true` or `false`                                                     | Enables or disables auto-fixing of rule violations                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| `fixable`            | Rules that are allowed to auto-fix        | Array of rule codes                                                            | Specific rules that are allowed to make auto-fixes                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| `unfixable`          | Rules that are not allowed to auto-fix    | Array of rule codes                                                            | Specific rules that shouldn't make auto-fixes                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| `respect-gitignore`  | Respect .gitignore file                   | Boolean: `true` or `false` (Default: `true`)                                   | Whether to ignore files listed in .gitignore                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| `cache-dir`          | Directory for caching                     | String path like `".ruff_cache"`                                               | Directory where Ruff will store cache data                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| `dummy-variable-rgx` | Regex for dummy variables                 | String regex like `"^(_+\|dummy)$"`                                            | Regex pattern for variables that should be considered "dummy" variables                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |

### Per-File Ignores Section

The `[per-file-ignores]` section lets you specify different rules to ignore for specific files or file patterns.

| Parameter Example     | Description                              | Possible Values                             | Meaning                                                                                                                               |
| --------------------- | ---------------------------------------- | ------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| `"__init__.py"`       | Rules to ignore in `__init__.py` files   | Array of rule codes like `["F401"]`         | Common to ignore unused imports (`F401`) in `__init__.py` since they're often used to expose internal modules                         |
| `"test_*.py"`         | Rules to ignore in test files            | Array of rule codes like `["E501", "S101"]` | Test files often have long lines or use assert statements, so it's common to ignore `E501` (line too long) and `S101` (use of assert) |
| `"docs/*.py"`         | Rules to ignore in example files in docs | Array of rule codes                         | Documentation files might have simplified examples that don't follow all standards                                                    |
| `"**/generated/*.py"` | Rules to ignore in generated files       | Array of rule codes like `["ALL"]`          | Generated files might not follow standards, `"ALL"` ignores all rules for these files                                                 |

### Format Section

The `[format]` section controls code formatting options.

| Parameter                    | Description                          | Possible Values                        | Meaning                                                                                                                            |
| ---------------------------- | ------------------------------------ | -------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| `quote-style`                | String quote style                   | `"single"`, `"double"`, or `"default"` | The quote character to use for strings. `"default"` follows Python conventions (double for docstrings, single for regular strings) |
| `indent-style`               | Indentation style                    | `"space"` or `"tab"`                   | Whether to use spaces or tabs for indentation                                                                                      |
| `line-ending`                | Line ending style                    | `"auto"`, `"lf"`, `"crlf"`, or `"cr"`  | End-of-line character(s): `"auto"` (respect existing), `"lf"` (Unix-style), `"crlf"` (Windows-style), or `"cr"` (classic Mac)      |
| `docstring-code-format`      | Format code blocks in docstrings     | Boolean: `true` or `false`             | Whether to format code blocks within docstrings                                                                                    |
| `docstring-code-line-length` | Line length in docstring code blocks | Integer                                | Maximum line length for code blocks in docstrings, if different from global `line-length`                                          |
| `skip-magic-trailing-comma`  | Skip magic trailing comma            | Boolean: `true` or `false`             | Whether to omit trailing commas in places where they would change Python's behavior                                                |

### Lint.isort Section

The `[lint.isort]` section controls import sorting options.

| Parameter                 | Description                           | Possible Values                                                          | Meaning                                                                         |
| ------------------------- | ------------------------------------- | ------------------------------------------------------------------------ | ------------------------------------------------------------------------------- |
| `known-first-party`       | Modules to consider as first-party    | Array of string module names like `["my_package"]`                       | Project-specific modules that should be grouped as first-party imports          |
| `known-third-party`       | Modules to consider as third-party    | Array of string module names like `["numpy", "pandas"]`                  | External modules that should be grouped as third-party imports                  |
| `required-imports`        | Imports that should always be present | Array of import statements like `["from __future__ import annotations"]` | Import statements that should be automatically added to all files               |
| `combine-as-imports`      | Combine as imports                    | Boolean: `true` or `false`                                               | Whether to combine import statements with the same source but different symbols |
| `split-on-trailing-comma` | Split on trailing comma               | Boolean: `true` or `false`                                               | Whether to split imports on trailing commas                                     |
| `relative-imports-order`  | Order for relative imports            | `"closest-to-furthest"` or `"furthest-to-closest"`                       | Order for relative imports based on their level                                 |
| `extra-standard-library`  | Additional standard library modules   | Array of string module names                                             | Modules to treat as part of the standard library                                |
| `case-sensitive`          | Case sensitivity for ordering         | Boolean: `true` or `false`                                               | Whether import sorting is case-sensitive                                        |

### Lint Section

The `[lint]` section controls general linting behavior and rule-specific options.

| Parameter                                       | Description                                   | Possible Values                   | Meaning                                                                  |
| ----------------------------------------------- | --------------------------------------------- | --------------------------------- | ------------------------------------------------------------------------ |
| `explicit-string-type`                          | Warn when string type annotations are unclear | Boolean: `true` or `false`        | Whether to warn when string type annotations could be ambiguous          |
| `pydocstyle.convention`                         | Docstring style convention                    | `"google"`, `"numpy"`, `"pep257"` | The docstring style convention to follow                                 |
| `flake8-quotes.style`                           | Quote style to enforce                        | `"single"`, `"double"`            | The quote style that flake8-quotes should enforce                        |
| `pylint.max-args`                               | Maximum arguments for functions               | Integer                           | Maximum number of arguments allowed for functions and methods            |
| `flake8-bugbear.extend-immutable-calls`         | Additional immutable call functions           | Array of strings                  | Add function names that should be treated as returning immutable objects |
| `isort.required-imports`                        | Required imports for every file               | Array of strings                  | Import statements that should be present in every file                   |
| `mccabe.max-complexity`                         | Maximum cyclomatic complexity                 | Integer (typically 10-15)         | Maximum complexity threshold for functions                               |
| `pycodestyle.max-doc-length`                    | Maximum docstring line length                 | Integer                           | Maximum line length specifically for docstrings                          |
| `flake8-pytest-style.fixture-parentheses`       | Fixture call style                            | Boolean: `true` or `false`        | Whether pytest fixture decorators require parentheses                    |
| `flake8-unused-arguments.ignore-variadic-names` | Ignore variadic args                          | Boolean: `true` or `false`        | Whether to ignore unused variadic arguments (like \*args, \*\*kwargs)    |
| `pyupgrade.keep-runtime-typing`                 | Keep runtime typing                           | Boolean: `true` or `false`        | Whether to preserve imports needed for runtime typing                    |
| `flake8-annotations.allow-star-arg-any`         | Allow \*args: Any                             | Boolean: `true` or `false`        | Whether to allow `*args: Any` in type annotations                        |

### Notes

- The parameters listed are the most common and important ones, but Ruff supports many more specific options.
- Rule codes can be precise (e.g., `"E501"`) or general (e.g., `"E"` for all pycodestyle errors).
- For a complete reference of all rules, see [the Ruff documentation](https://docs.astral.sh/ruff/rules/).
- Most rule groups can be further configured with specific settings in their own sections.
