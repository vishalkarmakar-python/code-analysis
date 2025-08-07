"""
Initializes the 'app' package and defines its public API.

By specifying `__all__`, we explicitly declare which names should be
imported when a client uses `from app import *`. This is a best practice
for package development, making the package's interface clear.
"""

from app.code_analysis import Analysis
from app.create_document import CreateDocument
from app.document_loader import Document_Loader
from app.document_splitter import Document_Splitter
from app.language_model import Ollama
from app.language_separator import ABAP
from app.prompt_generator import PromptGenerator
from app.structured_output import Code_Analysis
from typing import List

# The list of class names to be exposed when the package is imported.
__all__: List[str] = [
    "ABAP",
    "Document_Loader",
    "Document_Splitter",
    "Ollama",
    "PromptGenerator",
    "Analysis",
    "Code_Analysis",
    "CreateDocument",
]
