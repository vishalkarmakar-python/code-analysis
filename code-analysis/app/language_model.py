from contextlib import contextmanager
from dotenv import load_dotenv
from langchain_core.messages.base import BaseMessage
from langchain_ollama import ChatOllama
from logging import Logger, getLogger
from os import getenv
from typing import Any, ClassVar, Dict, Generator, List, Literal, Optional, Self


class Ollama:
    _instance: ClassVar[Self | None] = None
    _model_name: ClassVar[str | None] = None  # Track which model was initialized

    def __new__(cls, model_name: str) -> Self:
        if cls._instance is None:
            cls._instance = super(Ollama, cls).__new__(cls)
            cls._model_name = model_name
        elif cls._model_name != model_name:
            # Log warning about model name mismatch in singleton
            logger: Logger = getLogger(__name__)
            logger.warning(
                f"Ollama singleton already initialized with model '{cls._model_name}'. "
                f"Ignoring new model name '{model_name}'. Use separate instances if needed."
            )
        return cls._instance

    def __init__(self, model_name: str) -> None:
        if not hasattr(self, "_initialized"):
            # Set up logging for debugging and error tracking
            self._logger: Logger = getLogger(__name__)
            self._model_identifier: str = model_name

            # Initialize state flags
            self._initialized: bool = False
            self._is_connected: bool = False

            try:
                # Load and validate environment variables
                if self._load_environment_variables(model_name=model_name):
                    # Extract configuration from loaded environment variables
                    self._model: str = self._config[f"OLLAMA_MODEL_{model_name}"]
                    self._base_url: str = self._config["OLLAMA_MODEL_BASE_URL"]
                    self._temperature: float = self._config["OLLAMA_MODEL_TEMPERATURE"]

                    # Create the ChatOllama instance with loaded configuration
                    self._llm: ChatOllama = self._create_llm_instance()

                    # Test the connection to ensure model is accessible
                    self._is_connected = self._test_connection()

                    # Mark as successfully initialized
                    self._initialized = True
                    self._logger.info(f"Ollama initialized successfully with model: {self._model}")
                else:
                    raise RuntimeError("Failed to load required environment variables")

            except Exception as error:
                self._logger.error(f"Ollama initialization failed: {str(error)}")
                raise

    def _load_environment_variables(self, model_name: str) -> bool:
        self._config: Dict[str, Any] = {}

        # Define required environment variable names
        required_vars: List[str] = [
            f"OLLAMA_MODEL_{model_name}",
            "OLLAMA_MODEL_BASE_URL",
            "OLLAMA_MODEL_TEMPERATURE",
        ]

        try:
            # Attempt to load environment variables from .env file
            if not load_dotenv():
                self._logger.error("Failed to load environment variables from .env file")
                return False

            # Extract all required configuration values from environment
            for var in required_vars:
                value: str | None = getenv(key=var)
                if value is None:
                    raise Exception(f"Missing required environment variable: {var}")
                self._config[var] = value

            # Convert temperature to float with validation
            try:
                temp_value = float(self._config["OLLAMA_MODEL_TEMPERATURE"])
                if not (0.0 <= temp_value <= 2.0):
                    raise ValueError("Temperature must be between 0.0 and 2.0")
                self._config["OLLAMA_MODEL_TEMPERATURE"] = temp_value
            except ValueError as e:
                raise Exception(f"Invalid temperature value: {e}")

            self._logger.debug(f"Successfully loaded {len(required_vars)} environment variables")
            return True

        except Exception as error:
            self._logger.error(f"Environment variable loading failed: {str(error)}")
            raise

    def _create_llm_instance(self) -> ChatOllama:
        try:
            # Create ChatOllama instance with loaded configuration
            llm_instance = ChatOllama(
                model=self._model,  # Model name (e.g., "llama3.1:8b")
                base_url=self._base_url,  # Ollama service URL
                temperature=self._temperature,  # Response randomness (0.0-2.0)
            )

            self._logger.debug(f"ChatOllama instance created successfully for model: {self._model}")
            return llm_instance

        except Exception as error:
            self._logger.error(f"Failed to create ChatOllama instance: {error}")
            raise

    def _test_connection(self) -> bool:
        # Ensure LLM instance exists before testing
        assert self._llm is not None, "Ollama model is not initialized"

        try:
            # Send a simple test message to verify connectivity
            test_message: str = "Hello, this is a connection test."
            response: BaseMessage = self._llm.invoke(input=test_message)

            # Validate that we received a proper response
            if response and response.content:
                self._logger.info("Model connection test successful")

                # Log response preview for debugging (first 100 characters)
                if isinstance(response.content, str):
                    preview: str = response.content[:100]
                    self._logger.debug(f"Test response preview: {preview}...")

                return True
            else:
                self._logger.warning("Model connection test returned empty response")
                return False

        except Exception as error:
            self._logger.error(f"Model connection test failed: {str(error)}")
            return False

    def get_token_count(self, content: str) -> int:
        return self._llm.get_num_tokens(text=content)

    @contextmanager
    def get_llm(self) -> Generator[ChatOllama, None, None]:
        # Ensure LLM is properly initialized before yielding
        if not self._initialized or not hasattr(self, "_llm"):
            raise Exception("LLM not initialized. Check initialization status.")

        try:
            # Yield the ChatOllama instance for use
            yield self._llm
        except Exception as error:
            # Log any errors that occur during LLM operations
            self._logger.error(f"LLM operation error: {str(error)}")
            raise

    def __enter__(self) -> Self:
        if not self._initialized:
            raise Exception("LLM not initialized. Check initialization status.")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if exc_type is not None:
            # Log any exceptions that occurred in the context
            self._logger.error(f"Exception occurred in Ollama context: {exc_type.__name__}: {exc_val}")
        # Return None to allow exceptions to propagate normally
        return None

    @property
    def is_initialized(self) -> bool:
        return getattr(self, "_initialized", False)

    @property
    def get_llm_instance(self) -> ChatOllama:
        if not getattr(self, "_initialized", False):
            raise RuntimeError("LLM instance is not initialized. Ensure the Ollama class was properly instantiated with valid configuration.")

        if not hasattr(self, "_llm"):
            raise RuntimeError("LLM instance is missing. This indicates an initialization error.")

        return self._llm

    @property
    def connection_exists(self) -> bool:
        return getattr(self, "_is_connected", False)

    @property
    def model_name(self) -> Optional[str]:
        return getattr(self, "_model", None)

    @property
    def base_url(self) -> Optional[str]:
        return getattr(self, "_base_url", None)

    @property
    def temperature(self) -> Optional[float]:
        return getattr(self, "_temperature", None)

    @property
    def model_identifier(self) -> Optional[str]:
        return getattr(self, "_model_identifier", None)

    def __repr__(self) -> str:
        status: Literal["initialized"] | Literal["not initialized"] = "initialized" if self.is_initialized else "not initialized"
        model: str = self.model_name or "unknown"
        return f"Ollama(model='{model}', status='{status}')"
