from tiktoken import Encoding, get_encoding, list_encoding_names
from typing import ClassVar, List, Self


class CL100K:
    _instance: ClassVar[Self | None] = None

    def __new__(cls, model_name: str) -> Self:
        if cls._instance is None:
            cls._instance = super(CL100K, cls).__new__(cls)
        return cls._instance

    @staticmethod
    def calculate_token(page_content: str) -> int:
        encoder_list: List[str] = list_encoding_names()
        if "cl100k_base" in encoder_list:
            encoding: Encoding = get_encoding("cl100k_base")
            tokens: List[int] = encoding.encode(page_content)
            return len(tokens)
        else:
            return 0
