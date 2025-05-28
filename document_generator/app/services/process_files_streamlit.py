from app.schema.schema_file import SchemaFile
from os import path
from streamlit.runtime.uploaded_file_manager import UploadedFile
from typing import List, Optional


class File_Processor_Streamlit:
    @staticmethod
    def generate_code_file_list(
        code_file_list: Optional[List[UploadedFile]],
        code_file_path: Optional[str],
    ) -> List[SchemaFile]:
        file_details_list: List[SchemaFile] = []

        if code_file_list and code_file_path:
            for code_file in code_file_list:
                file_details_list.append(
                    SchemaFile(
                        file_name=code_file.name,
                        file_path=path.join(code_file_path, code_file.name),
                        file_type=path.splitext(code_file.name)[1][1:],  # get file extension without dot
                        file_size=code_file.size,
                    )
                )
        return file_details_list

    @staticmethod
    def generate_spec_file_list(
        spec_file_list: Optional[List[UploadedFile]],
        spec_file_path: Optional[str],
    ) -> List[SchemaFile]:
        file_details_list: List[SchemaFile] = []

        if spec_file_list and spec_file_path:
            for spec_file in spec_file_list:
                file_details_list.append(
                    SchemaFile(
                        file_name=spec_file.name,
                        file_path=path.join(spec_file_path, spec_file.name),
                        file_type=path.splitext(spec_file.name)[1][1:],  # get file extension without dot
                        file_size=spec_file.size,
                    )
                )
        return file_details_list
