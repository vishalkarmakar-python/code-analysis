from contextlib import contextmanager
from dotenv import load_dotenv
from langchain_core.messages.base import BaseMessage
from langchain_ollama import ChatOllama
from logging import Logger, getLogger
from os import getenv
from typing import Any, ClassVar, Dict, Generator, List, Optional, Self


class Ollama:
    _instance: ClassVar[Self | None] = None

    def __new__(cls, model_name: str) -> Self:
        if cls._instance is None:
            cls._instance = super(Ollama, cls).__new__(cls)
        return cls._instance

    def __init__(self, model_name: str) -> None:
        if not hasattr(self, "_initialized"):
            # Set up logging for debugging and error tracking
            self._logger: Logger = getLogger(__name__)
            # Load and validate environment variables
            if self._load_environment_variables(model_name=model_name):
                # Extract configuration from loaded environment variables
                self._model: str = self._config[f"OLLAMA_MODEL_{model_name}"]
                self._base_url: str = self._config["OLLAMA_MODEL_BASE_URL"]
                self._temperature: Optional[float] = self._config["OLLAMA_MODEL_TEMPERATURE"]
                # Create the ChatOllama instance with loaded configuration
                self._llm: ChatOllama = self._create_llm_instance()
                # Test the connection to ensure model is accessible
                self._is_connected: bool = self._test_connection()
                # Mark as successfully initialized
                self._initialized = True
                self._logger.info(f"{model_name} initialized successfully with model: {self._model}")
                # return True
            else:
                self._logger.error("Failed to load required environment variables")

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
            if load_dotenv():
                # Extract all required configuration values from environment
                for var in required_vars:
                    self._config[var] = getenv(key=var)

                # Check for any missing required variables
                missing_vars: List[str] = [var for var, value in self._config.items() if var in required_vars and value is None]

                if missing_vars:
                    raise Exception(f"Missing required environment variables: {', '.join(missing_vars)}")

                self._logger.debug(f"Successfully loaded {len(required_vars)} environment variables")
                return True
            else:
                self._logger.error("Failed to load environment variables from .env file")
                return False

        except Exception as error:
            self._logger.error(f"Environment variable loading failed: {str(error)}")
            raise

    def _create_llm_instance(self) -> ChatOllama:
        try:
            # Create ChatOllama instance with loaded configuration
            llm_instance = ChatOllama(
                model=self._model,  # Model name (e.g., "llama3.1:8b")
                base_url=self._base_url,  # Ollama service URL
                temperature=self._temperature,  # Response randomness (0.0-1.0)
            )

            self._logger.debug(f"ChatOllama instance created successfully for model: {self._model}")
            return llm_instance

        except Exception as error:
            self._logger.error(f"Failed to create ChatOllama instance: {error}")
            raise

    def _test_connection(self) -> bool:
        # Ensure LLM instance exists before testing
        assert self._llm is not None, "Llama3 model is not initialized"

        try:
            # Send a simple test message to verify connectivity
            test_message: str = "Hello, this is a connection test."
            response: BaseMessage = self._llm.invoke(input=test_message)

            # Validate that we received a proper response
            if response and response.content:
                self._logger.info("Model connection test successful")

                # Log response preview for debugging (first 100 characters)
                if isinstance(response.content, str):
                    preview = response.content[:100]
                    self._logger.debug(f"Test response preview: {preview}...")

                return True
            else:
                self._logger.warning("Model connection test returned empty response")
                return False

        except Exception as error:
            self._logger.error(f"Model connection test failed: {str(error)}")
            return False

    @contextmanager
    def get_llm(self) -> Generator[ChatOllama, None, None]:
        """
        Context manager for safely accessing the ChatOllama instance.

        Provides safe access to the underlying ChatOllama instance with
        proper error handling and resource management.

        Yields:
            ChatOllama: The initialized ChatOllama instance

        Raises:
            Exception: If LLM is not initialized or if an error occurs during operation

        Example:
            >>> llama = Llama3()
            >>> llama.initialize_llm("LLAMA")
            >>> with llama.get_llm() as model:
            ...     response = model.invoke("What is the capital of France?")
            ...     print(response.content)

        Note:
            This context manager ensures that any errors during LLM operations
            are properly logged and propagated while maintaining resource safety.
        """
        # Ensure LLM is properly initialized before yielding
        if self._initialized and self._llm:
            try:
                # Yield the ChatOllama instance for use
                yield self._llm
            except Exception as error:
                # Log any errors that occur during LLM operations
                self._logger.error(f"LLM operation error: {str(error)}")
                raise
        else:
            raise Exception("LLM not initialized. Call initialize_llm() first.")

    def __enter__(self) -> Self:
        if not self._initialized:
            raise Exception("LLM not initialized. Call initialize_llm() first.")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if exc_type is not None:
            # Log any exceptions that occurred in the context
            self._logger.error(f"Exception occurred in Llama3 context: {exc_type.__name__}: {exc_val}")
        # Return None to allow exceptions to propagate normally
        return None

    @property
    def is_initialized(self) -> bool:
        """Check if the Gemma3 LLM client is initialized."""
        return self._initialized

    @property
    def connection_exists(self) -> bool:
        return self._is_connected

    @property
    def model_name(self) -> Optional[str]:
        return self._model if hasattr(self, "_model") else None

    @property
    def base_url(self) -> Optional[str]:
        return self._base_url if hasattr(self, "_base_url") else None

    @property
    def temperature(self) -> Optional[float]:
        return self._temperature if hasattr(self, "_temperature") else None

    # def __init__(self) -> None:
    #     if not hasattr(self, "_initialized"):
    #         # Set up logging for debugging and error tracking
    #         self._logger: Logger = getLogger(__name__)

    #         # Core Ollama Model configuration attributes
    #         self._llm: ChatOllama  # Will be set during initialization
    #         self._model: str  # Model name (e.g., "llama3.1:8b")
    #         self._base_url: str  # Ollama service URL (e.g., "http://localhost:11434")
    #         self._temperature: Optional[float] = None  # Model temperature (0.0-1.0)

    #         # State management flags
    #         self._is_connected: bool = False  # Connection status flag
    #         self._initialized: bool = False  # Initialization completion flag

    #         # Configuration storage
    #         self._config: Dict[str, Any] = {}  # Environment variables storage

    # def initialize_llm(self, model_name: str) -> bool:
    #     try:
    #         # Load and validate environment variables
    #         if self._load_environment_variables(model_name=model_name):
    #             # Extract configuration from loaded environment variables
    #             self._model = self._config[f"OLLAMA_MODEL_{model_name}"]
    #             self._base_url = self._config["OLLAMA_MODEL_BASE_URL"]
    #             self._temperature = self._config["OLLAMA_MODEL_TEMPERATURE"]

    #             # Create the ChatOllama instance with loaded configuration
    #             self._llm = self._create_llm_instance()

    #             # Test the connection to ensure model is accessible
    #             self._is_connected = self._test_connection()

    #             # Mark as successfully initialized
    #             self._initialized = True

    #             self._logger.info(f"{model_name} initialized successfully with model: {self._model}")
    #             return True
    #         else:
    #             self._logger.error("Failed to load required environment variables")
    #             return False

    #     except Exception as error:
    #         self._logger.error(f"Initialization failed: {str(error)}")
    #         return False
