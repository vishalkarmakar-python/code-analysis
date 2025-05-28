from langchain_community.document_loaders import TextLoader
from langchain_core.documents.base import Document
from typing import Any, List


class TextDocumentLoader:
    @staticmethod
    def load_text_documents(file_list: List[Any]) -> List[Document]:
        loaded_documents: List[Document] = []
        if not file_list:
            print("Empty file list provided for text documents.")
            return loaded_documents

        for file_info in file_list:
            try:
                file_path: str = file_info.file_path
                text_loader: TextLoader = TextLoader(
                    file_path=file_path,
                    encoding="utf-8",
                    autodetect_encoding=True,
                )
                loaded_documents.extend(text_loader.load())
            except AttributeError:
                print(f"Error accessing 'file_path' for an item in file_list. Item: {file_info}")
            except Exception as error:
                # Error message from the original TextDocumentLoader
                print(f"Error loading file {getattr(file_info, 'file_path', 'unknown')}: {str(error)}")

        return loaded_documents
