"""
Manages the connection and interaction with an Ollama Language Model.

This module provides a singleton class `Ollama` that encapsulates the
configuration, initialization, and interaction with a `ChatOllama` instance
from LangChain. It handles loading settings from environment variables,
testing the connection, and providing access to the LLM instance.
"""

from contextlib import contextmanager
from dotenv import load_dotenv
from langchain_core.messages.base import BaseMessage
from langchain_ollama import ChatOllama
from os import getenv
from tiktoken import Encoding, get_encoding
from typing import Any, ClassVar, Dict, Generator, List, Literal, Self


class Ollama:
    """
    A singleton wrapper for the LangChain ChatOllama client.

    This class ensures that only one instance of the LLM client exists for a
    given model name. It loads configuration from a .env file, initializes the
    model, and provides methods for token counting and interaction.

    Attributes:
        _instance: The singleton instance of the class.
        _model_name: The name of the model the singleton is initialized with.
    """

    _instance: ClassVar[Self | None] = None
    _model_name: ClassVar[str | None] = None  # Track which model was initialized

    def __new__(cls, model_name: str) -> Self:
        """
        Creates a new instance if one doesn't exist, otherwise returns the existing one.

        This implementation of the singleton pattern warns the user if an attempt
        is made to re-initialize the singleton with a different model name.

        Args:
            model_name: The name of the Ollama model to use (e.g., "QWEN").

        Returns:
            The singleton instance of the Ollama class.
        """
        if cls._instance is None:
            cls._instance = super(Ollama, cls).__new__(cls)
            cls._model_name = model_name
        elif cls._model_name != model_name:
            print(
                f"[WARNING] Ollama singleton already initialized with model '{cls._model_name}'. "
                f"Ignoring new model name '{model_name}'. Use separate instances if needed."
            )
        return cls._instance

    def __init__(self, model_name: str) -> None:
        """
        Initializes the Ollama instance on its first creation.

        Loads environment variables, creates the ChatOllama instance, and tests
        the connection. This constructor will only run its full logic once.

        Args:
            model_name: The identifier for the model configuration to load.

        Raises:
            RuntimeError: If loading environment variables or initializing the LLM fails.
        """
        # The hasattr check ensures this heavy initialization logic runs only once.
        if not hasattr(self, "_initialized"):
            self._model_identifier: str = model_name
            self._initialized: bool = False
            self._is_connected: bool = False

            try:
                # Load and validate environment variables from .env file.
                if self._load_environment_variables(model_name=model_name):
                    # Extract configuration into class attributes.
                    self._model: str = self._config[f"OLLAMA_MODEL_{model_name}"]
                    self._model_max_tokens: int = self._config[f"OLLAMA_MODEL_{model_name}_MAX_TOKENS"]
                    self._model_max_chunk: int = self._config[f"OLLAMA_MODEL_{model_name}_MAX_CHUNK"]
                    self._model_max_gpu: int = self._config["OLLAMA_GPU"]
                    self._model_base_url: str = self._config["OLLAMA_MODEL_BASE_URL"]
                    self._model_temperature: float = self._config["OLLAMA_MODEL_TEMPERATURE"]

                    # Create the LangChain ChatOllama instance.
                    self._llm: ChatOllama = self._create_llm_instance()
                    # Verify that the application can communicate with the LLM server.
                    self._is_connected = self._test_connection()
                    # Mark as successfully initialized.
                    self._initialized = True
                    print(f"[INFO] Ollama initialized successfully with model: {self._model}")
                else:
                    raise RuntimeError("Failed to load required environment variables")

            except Exception as error:
                print(f"[ERROR] Ollama initialization failed: {str(error)}")
                raise

    def _load_environment_variables(self, model_name: str) -> bool:
        """
        Loads required configuration from a .env file.

        Args:
            model_name: The model name used to find specific env vars like
                        `OLLAMA_MODEL_{model_name}`.

        Returns:
            True if all required variables were loaded successfully, False otherwise.

        Raises:
            Exception: If any required environment variable is missing or invalid.
        """
        self._config: Dict[str, Any] = {}
        # Define the expected environment variable keys.
        required_vars: List[str] = [
            f"OLLAMA_MODEL_{model_name}",
            f"OLLAMA_MODEL_{model_name}_MAX_TOKENS",
            f"OLLAMA_MODEL_{model_name}_MAX_CHUNK",
            "OLLAMA_MODEL_BASE_URL",
            "OLLAMA_MODEL_TEMPERATURE",
            "OLLAMA_GPU",
        ]

        try:
            load_dotenv()  # Load variables from .env file in the project root.
            for var in required_vars:
                value: str | None = getenv(key=var)
                if value is None:
                    raise Exception(f"Missing required environment variable: {var}")
                self._config[var] = value

            # Validate and convert specific variables to their correct types.
            self._config[f"OLLAMA_MODEL_{model_name}_MAX_TOKENS"] = int(self._config[f"OLLAMA_MODEL_{model_name}_MAX_TOKENS"])
            self._config[f"OLLAMA_MODEL_{model_name}_MAX_CHUNK"] = int(self._config[f"OLLAMA_MODEL_{model_name}_MAX_CHUNK"])
            self._config["OLLAMA_GPU"] = int(self._config["OLLAMA_GPU"])
            self._config["OLLAMA_MODEL_TEMPERATURE"] = float(self._config["OLLAMA_MODEL_TEMPERATURE"])

            print(f"[DEBUG] Successfully loaded {len(required_vars)} environment variables")
            return True

        except Exception as error:
            print(f"[ERROR] Environment variable loading failed: {str(error)}")
            raise

    def _create_llm_instance(self) -> ChatOllama:
        """
        Initializes the ChatOllama object with the loaded configuration.

        Returns:
            An instance of `langchain_ollama.ChatOllama`.
        """
        try:
            llm_instance = ChatOllama(
                model=self._model,
                base_url=self._model_base_url,
                temperature=self._model_temperature,
                num_ctx=self._model_max_tokens,
                num_gpu=self._model_max_gpu,
                num_predict=4096,  # Max tokens to generate in a single response
                top_k=10,  # A lower value makes the output more deterministic
                top_p=0.5,  # Nucleus sampling
            )
            print(f"[DEBUG] ChatOllama instance created successfully for model: {self._model}")
            return llm_instance
        except Exception as error:
            print(f"[ERROR] Failed to create ChatOllama instance: {error}")
            raise

    def _test_connection(self) -> bool:
        """
        Sends a simple test prompt to the LLM to verify connectivity.

        Returns:
            True if a valid response is received, False otherwise.
        """
        assert self._llm is not None, "Ollama model is not initialized"
        try:
            test_message: str = "Hello, this is a connection test. Respond with a single word."
            response: BaseMessage = self._llm.invoke(input=test_message)
            if response and response.content:
                print("[INFO] Model connection test successful")
                return True
            else:
                print("[WARNING] Model connection test returned empty response")
                return False
        except Exception as error:
            print(f"[ERROR] Model connection test failed: {str(error)}")
            return False

    @staticmethod
    def count_tokens(content: str) -> int:
        """
        Counts the number of tokens in a string using the tiktoken library.

        This is a static method so it can be used without an instance of the class.
        It uses the 'cl100k_base' encoding, which is standard for many modern models.

        Args:
            content: The text content to be tokenized.

        Returns:
            The number of tokens as an integer.
        """
        try:
            encoding: Encoding = get_encoding("cl100k_base")
            return len(encoding.encode(content))
        except Exception as error:
            print(f"[ERROR] Tiktoken counting failed: {error}")
            return len(content)  # Fallback to character count

    @contextmanager
    def get_llm(self) -> Generator[ChatOllama, None, None]:
        """
        Provides the ChatOllama instance within a context manager.

        This is the recommended way to access the LLM instance to ensure
        proper handling of resources and exceptions.

        Yields:
            The `ChatOllama` instance.

        Raises:
            Exception: If the LLM is not initialized.
        """
        if not self._initialized or not hasattr(self, "_llm"):
            raise Exception("LLM not initialized. Check initialization status.")
        try:
            yield self._llm
        except Exception as error:
            print(f"[ERROR] LLM operation error: {str(error)}")
            raise

    @property
    def model_max_token(self) -> int:
        """Returns the maximum token limit for the model."""
        return int(getattr(self, "_model_max_tokens", 0))

    # Other properties and methods...
    @property
    def is_initialized(self) -> bool:
        """Checks if the instance has been successfully initialized."""
        return getattr(self, "_initialized", False)

    def __repr__(self) -> str:
        """Provides a developer-friendly string representation of the object."""
        status: Literal["initialized"] | Literal["not initialized"] = "initialized" if self.is_initialized else "not initialized"
        model: str = self._model_name or "unknown"
        return f"Ollama(model='{model}', status='{status}')"
