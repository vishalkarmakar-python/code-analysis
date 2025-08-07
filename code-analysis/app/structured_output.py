"""
Defines the Pydantic models for structured output from the LLM.

Using Pydantic models with LangChain's `with_structured_output` method
forces the LLM to return a JSON object that conforms to a predefined schema.
This makes the output reliable and easy to parse.
"""

from pydantic import BaseModel, Field

# Field descriptions guide the LLM on what content to generate for each field.
_analysis: str = "A detailed, technical breakdown of the code chunk. Explain the logic, flow, and purpose of every code block."
_summary: str = "A high-level summary of the code chunk's overall purpose and functionality."


class Code_Analysis(BaseModel):
    """
    Defines the expected structure for the analysis of a single code chunk.
    The LLM is instructed to fill out these two fields based on its analysis.
    """

    analysis: str = Field(description=_analysis)
    summary: str = Field(description=_summary)
