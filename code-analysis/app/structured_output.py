from pydantic import BaseModel, Field

_analysis: str = "Detailed analysis of the chunk, including technical aspects and purpose. Explain the entire working logic of all possible code blocks along with the flow."
_summary: str = (
    "Detailed summary of the ABAP Code chunk content including explanation the entire working logic of all possible code blocks along with the flow."
)


class Code_Analysis(BaseModel):
    analysis: str = Field(description=_analysis)
    summary: str = Field(description=_summary)


class Single_Chunk(BaseModel):
    content: str = Field(description="The content of the chunk.")
    summary: str = Field(description=_summary)
    object_type: str = Field(description="Type of the ABAP object identified in the chunk.")
    analysis: str = Field(description=_analysis)
