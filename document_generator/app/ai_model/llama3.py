"""
Llama3 ChatOllama Integration Module

This module provides a singleton wrapper for managing Llama3 ChatOllama connections
with proper initialization, configuration management, and connection testing.

Classes:
    Llama3: Singleton class for managing Llama3 ChatOllama connections

Example:
    Basic usage:
        llama = Llama3()
        if llama.initialize_llm("LLAMA"):
            with llama.get_llm() as model:
                response = model.invoke("Hello, world!")

    Context manager usage:
        llama = Llama3()
        llama.initialize_llm("LLAMA")
        with llama as instance:
            with instance.get_llm() as model:
                response = model.invoke("Hello, world!")
"""

from contextlib import contextmanager
from dotenv import load_dotenv
from langchain_core.messages import BaseMessage
from langchain_ollama import ChatOllama
from logging import Logger, getLogger
from os import getenv
from typing import Any, ClassVar, Dict, Generator, List, Optional, Self


class Llama3:
    """
    Singleton class for managing Llama3 ChatOllama connections.

    This class ensures only one instance of the Llama3 connection exists
    throughout the application lifecycle, providing efficient resource management
    and preventing multiple unnecessary connections to the Ollama service.

    The class implements the singleton pattern to ensure resource efficiency
    and provides context manager support for proper resource handling.

    Attributes:
        _instance (ClassVar[Optional[Self]]): Class-level singleton instance
        _logger (Logger): Logger instance for debugging and error tracking
        _llm (ChatOllama): The ChatOllama instance for model interactions
        _model (str): Name of the Llama model being used
        _base_url (str): Base URL for the Ollama service
        _temperature (Optional[float]): Temperature setting for model responses
        _is_connected (bool): Flag indicating successful connection status
        _initialized (bool): Flag indicating if the instance is properly initialized
        _config (Dict[str, Any]): Configuration dictionary storing environment variables

    Example:
        >>> llama = Llama3()
        >>> success = llama.initialize_llm("LLAMA")
        >>> if success and llama.connection_exists:
        ...     with llama.get_llm() as model:
        ...         response = model.invoke("Hello!")
    """

    # Class variable to hold the singleton instance
    _instance: ClassVar[Optional[Self]] = None

    def __new__(cls) -> Self:
        """
        Create or return existing singleton instance.

        Implements the singleton pattern by ensuring only one instance
        of the Llama3 class exists throughout the application lifecycle.

        Returns:
            Self: The singleton instance of Llama3

        Note:
            This method is called before __init__ and controls object creation.
            Subsequent calls to Llama3() will return the same instance.
        """
        if cls._instance is None:
            cls._instance = super(Llama3, cls).__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        """
        Initialize the Llama3 instance with default configuration.

        Sets up the initial state of the singleton instance, including
        logger configuration and instance variables. Uses a guard to
        prevent re-initialization of the singleton instance.

        Note:
            This method only runs once per singleton instance, even if
            Llama3() is called multiple times.
        """
        # Prevent re-initialization of singleton instance
        if not hasattr(self, "_initialized"):
            # Set up logging for debugging and error tracking
            self._logger: Logger = getLogger(__name__)

            # Core Ollama Model configuration attributes
            self._llm: ChatOllama  # Will be set during initialization
            self._model: str  # Model name (e.g., "llama3.1:8b")
            self._base_url: str  # Ollama service URL (e.g., "http://localhost:11434")
            self._temperature: Optional[float] = None  # Model temperature (0.0-1.0)

            # State management flags
            self._is_connected: bool = False  # Connection status flag
            self._initialized: bool = False  # Initialization completion flag

            # Configuration storage
            self._config: Dict[str, Any] = {}  # Environment variables storage

    def initialize_llm(self, model_name: str) -> bool:
        """
        Initialize the LLM with specified model configuration.

        Loads environment variables, creates the ChatOllama instance,
        and tests the connection to ensure everything is working properly.

        Args:
            model_name (str): Prefix for environment variable names
                            (e.g., "LLAMA" for LLAMA_MODEL, LLAMA_MODEL_BASE_URL, etc.)

        Returns:
            bool: True if initialization successful, False otherwise

        Environment Variables Required:
            {model_name}_MODEL: The Ollama model name (e.g., "llama3.1:8b")
            {model_name}_MODEL_BASE_URL: Ollama service URL (e.g., "http://localhost:11434")
            {model_name}_MODEL_TEMPERATURE: Model temperature as string (e.g., "0.7")

        Example:
            >>> llama = Llama3()
            >>> success = llama.initialize_llm("LLAMA")
            >>> if success:
            ...     print(f"Initialized with model: {llama.model_name}")

        Raises:
            Exception: If required environment variables are missing
        """
        try:
            # Load and validate environment variables
            if self._load_environment_variables(model_name=model_name):
                # Extract configuration from loaded environment variables
                self._model = self._config[f"{model_name}_MODEL"]
                self._base_url = self._config[f"{model_name}_MODEL_BASE_URL"]
                self._temperature = self._config[f"{model_name}_MODEL_TEMPERATURE"]

                # Create the ChatOllama instance with loaded configuration
                self._llm = self._create_llm_instance()

                # Test the connection to ensure model is accessible
                self._is_connected = self._test_connection()

                # Mark as successfully initialized
                self._initialized = True

                self._logger.info(f"Llama3 initialized successfully with model: {self._model}")
                return True
            else:
                self._logger.error("Failed to load required environment variables")
                return False

        except Exception as error:
            self._logger.error(f"Initialization failed: {str(error)}")
            return False

    def _load_environment_variables(self, model_name: str) -> bool:
        """
        Load and validate required environment variables from .env file.

        Attempts to load environment variables using python-dotenv and
        validates that all required variables are present and not None.

        Args:
            model_name (str): Prefix for environment variable names

        Returns:
            bool: True if all required variables loaded successfully, False otherwise

        Raises:
            Exception: If required environment variables are missing after loading

        Note:
            Expected environment variables:
            - {model_name}_MODEL: Model identifier
            - {model_name}_MODEL_BASE_URL: Service endpoint
            - {model_name}_MODEL_TEMPERATURE: Response randomness setting
        """
        # Define required environment variable names
        required_vars: List[str] = [
            f"{model_name}_MODEL",
            f"{model_name}_MODEL_BASE_URL",
            f"{model_name}_MODEL_TEMPERATURE",
        ]

        try:
            # Attempt to load environment variables from .env file
            if load_dotenv():
                # Extract all required configuration values from environment
                for var in required_vars:
                    self._config[var] = getenv(key=var)

                # Check for any missing required variables
                missing_vars: List[str] = [
                    var for var, value in self._config.items() if var in required_vars and value is None
                ]

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
        """
        Create and configure a ChatOllama instance.

        Uses the loaded configuration to instantiate a ChatOllama object
        with the specified model, base URL, and temperature settings.

        Returns:
            ChatOllama: Configured ChatOllama instance ready for use

        Raises:
            Exception: If ChatOllama instance creation fails

        Note:
            Temperature should be a float between 0.0 (deterministic) and 1.0 (random).
            The base_url should point to a running Ollama service instance.
        """
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
        """
        Test the connection to the Llama3 model with a simple query.

        Sends a test message to the model to verify that the connection
        is working properly and the model can respond appropriately.

        Returns:
            bool: True if connection test successful, False otherwise

        Raises:
            AssertionError: If _llm is not initialized before testing

        Note:
            This method helps identify connection issues early in the
            initialization process, allowing for graceful error handling.
        """
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
        """
        Context manager entry point.

        Allows the Llama3 instance to be used in a 'with' statement
        for proper resource management and error handling.

        Returns:
            Self: The Llama3 instance for chained operations

        Raises:
            Exception: If LLM is not initialized

        Example:
            >>> llama = Llama3()
            >>> llama.initialize_llm("LLAMA")
            >>> with llama as instance:
            ...     with instance.get_llm() as model:
            ...         response = model.invoke("Hello!")
        """
        if not self._initialized:
            raise Exception("LLM not initialized. Call initialize_llm() first.")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """
        Context manager exit point.

        Handles cleanup and logging when exiting the context manager.
        Logs any exceptions that occurred within the context.

        Args:
            exc_type: Exception type (if any)
            exc_val: Exception value (if any)
            exc_tb: Exception traceback (if any)

        Returns:
            None: Allows exceptions to propagate normally

        Note:
            This method ensures that any exceptions occurring within
            the context are properly logged for debugging purposes.
        """
        if exc_type is not None:
            # Log any exceptions that occurred in the context
            self._logger.error(f"Exception occurred in Llama3 context: {exc_type.__name__}: {exc_val}")
        # Return None to allow exceptions to propagate normally
        return None

    @property
    def connection_exists(self) -> bool:
        """
        Check if a valid connection to the model exists.

        Returns:
            bool: True if connection is established and tested, False otherwise

        Example:
            >>> llama = Llama3()
            >>> llama.initialize_llm("LLAMA")
            >>> if llama.connection_exists:
            ...     print("Ready to process requests")
        """
        return self._is_connected

    @property
    def model_name(self) -> Optional[str]:
        """
        Get the name of the currently configured model.

        Returns:
            Optional[str]: Model name if initialized, None otherwise

        Example:
            >>> llama = Llama3()
            >>> llama.initialize_llm("LLAMA")
            >>> print(f"Using model: {llama.model_name}")
        """
        return self._model if hasattr(self, "_model") else None

    @property
    def base_url(self) -> Optional[str]:
        """
        Get the base URL of the Ollama service.

        Returns:
            Optional[str]: Base URL if initialized, None otherwise

        Example:
            >>> llama = Llama3()
            >>> llama.initialize_llm("LLAMA")
            >>> print(f"Connected to: {llama.base_url}")
        """
        return self._base_url if hasattr(self, "_base_url") else None

    @property
    def temperature(self) -> Optional[float]:
        """
        Get the temperature setting for model responses.

        Returns:
            Optional[float]: Temperature value if initialized, None otherwise

        Note:
            Temperature controls response randomness:
            - 0.0: Deterministic responses
            - 1.0: Maximum randomness
            - Typical range: 0.1-0.9

        Example:
            >>> llama = Llama3()
            >>> llama.initialize_llm("LLAMA")
            >>> print(f"Temperature setting: {llama.temperature}")
        """
        return self._temperature if hasattr(self, "_temperature") else None
