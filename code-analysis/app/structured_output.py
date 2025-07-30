from pydantic import BaseModel, Field


class Single_Chunk(BaseModel):
    content: str = Field(description="The content of the chunk.")
    summary: str = Field(description="Summary of the chunk content.")
    object_type: str = Field(description="Type of the ABAP object identified in the chunk.")
    analysis: str = Field(description="Detailed analysis of the chunk, including technical aspects and purpose.")


class Analysis_Chunk(BaseModel):
    summary: str = Field(description="Summary of the chunk content.")
    object_type: str = Field(description="Type of the ABAP object identified in the chunk.")
    analysis: str = Field(description="Detailed analysis of the chunk, including technical aspects and purpose.")
