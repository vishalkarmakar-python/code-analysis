from dotenv import load_dotenv
from langchain_core.messages.base import BaseMessage
from langchain_core.prompt_values import PromptValue
from langchain_ollama import ChatOllama
from os import getenv
from tiktoken import Encoding, get_encoding, list_encoding_names

# import tiktoken
from typing import ClassVar, List, Self


class Gemma3:
    _instance: ClassVar[Self | None] = None

    def __new__(cls) -> Self:
        if cls._instance is None:
            cls._instance = super(Gemma3, cls).__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if not hasattr(self, "_initialized"):
            if self._load_environment_variables():
                self._client = ChatOllama(
                    model=self._config["OLLAMA_MODEL"],
                    base_url=self._config["OLLAMA_MODEL_BASE_URL"],
                    temperature=self._config["OLLAMA_MODEL_TEMPERATURE"],
                )
                self._initialized = True
            else:
                self._initialized: bool = False
                raise ValueError("Failed to load environment variables for Gemma3.")

    def _load_environment_variables(self) -> bool:
        if load_dotenv():
            self._config: dict = {}
            required_vars: List[str] = [
                "OLLAMA_MODEL",
                "OLLAMA_MODEL_BASE_URL",
                "OLLAMA_MODEL_TEMPERATURE",
            ]
            # Get all required configuration values from environment
            for var in required_vars:
                self._config[var] = getenv(key=var)

            # # Check if any required values are missing
            missing_vars: List[str] = [var for var, value in self._config.items() if value is None]
            if missing_vars:
                raise Exception(f"Missing required environment variables: {', '.join(missing_vars)}")
            return True
        else:
            return False

    def invoke_llm(self, prompt: PromptValue) -> BaseMessage:
        return self._client.invoke(prompt)

    @staticmethod
    def calculate_token(page_content: str) -> int:
        encoder_list: List[str] = list_encoding_names()
        if "cl100k_base" in encoder_list:
            encoding: Encoding = get_encoding("cl100k_base")
            tokens: List[int] = encoding.encode(page_content)
            return len(tokens)
        else:
            return 0

    @property
    def is_initialized(self) -> bool:
        """Check if the Gemma3 LLM client is initialized."""
        return self._initialized
