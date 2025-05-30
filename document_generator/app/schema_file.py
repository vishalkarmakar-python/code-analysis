from pydantic import BaseModel


class SchemaFile(BaseModel):
    file_name: str
    file_path: str
    file_type: str
    file_size: int
