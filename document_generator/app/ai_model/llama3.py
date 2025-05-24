from langchain_core.messages.base import BaseMessage
from langchain_ollama import ChatOllama
from logging import INFO, Formatter, Logger, StreamHandler, getLogger
from typing import ClassVar, Optional, Self


class Llama3:
    """
    Singleton class for managing Llama3 ChatOllama connections.

    This class ensures only one instance of the Llama3 connection exists
    throughout the application lifecycle, providing efficient resource management.
    """

    _instance: ClassVar[Optional[Self]] = None

    def __new__(cls) -> Self:
        """
        Create or return existing singleton instance.

        Returns:
            Singleton instance of Llama3
        """
        if cls._instance is None:
            cls._instance = super(Llama3, cls).__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        """
        Initialize the Llama3 instance with default configuration.
        """
        # Prevent re-initialization of singleton
        if hasattr(self, "_initialized"):
            return

        self._initialized: bool = True
        # Default configuration
        self.model: str = "llama3.2:3b"
        self.base_url: str = "http://localhost:11434"
        self.temperature: float = 0.7
        self.llm: Optional[ChatOllama] = None
        self._is_connected: bool = False

        # Set up logging
        self.logger: Logger = getLogger(__name__)
        if not self.logger.handlers:
            handler = StreamHandler()
            formatter = Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(INFO)

    def _create_llm_instance(self) -> ChatOllama:
        """
        Create and configure ChatOllama instance.

        Returns:
            Configured ChatOllama instance

        Raises:
            Exception: If instance creation fails
        """
        try:
            return ChatOllama(
                model=self.model,
                base_url=self.base_url,
                temperature=self.temperature,
            )
        except Exception as e:
            self.logger.error(f"Failed to create ChatOllama instance: {e}")
            raise

    def connect(self) -> bool:
        """
        Establish connection to the Ollama server.

        Returns:
            True if connection is successful, False otherwise
        """
        if self._is_connected and self.llm is not None:
            self.logger.info("Already connected to Ollama server")
            return True

        try:
            self.llm = self._create_llm_instance()
            self._is_connected = True
            self.logger.info(f"Successfully connected to Ollama server at {self.base_url}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to connect to Ollama server: {e}")
            self._is_connected = False
            return False

    def test_connection(self, test_message: str = "Hello, how are you?") -> bool:
        """
        Test the connection to the Ollama server with a sample message.

        Args:
            test_message: Message to send for testing connection

        Returns:
            True if the connection test is successful, False otherwise
        """
        try:
            # Ensure connection is established
            if not self.connect():
                return False

            # Ensure llm is not None before invoking
            if self.llm is None:
                self.logger.error("LLM instance is None after connection")
                return False

            # Send test message
            response: BaseMessage = self.llm.invoke(input=test_message)
            self.logger.info("Connection test successful")

            # Handle different types of response content
            if isinstance(response.content, str):
                self.logger.info(f"Test response: {response.content[:100]}...")
            else:
                self.logger.info(f"Test response: {str(response.content)[:100]}...")

            return True

        except Exception as e:
            self.logger.error(f"Connection test failed: {e}")
            self._is_connected = False
            return False

    def invoke(self, message: str) -> Optional[str]:
        """
        Send a message to the Llama model and get response.

        Args:
            message: Input message to send to the model

        Returns:
            Model response content or None if failed
        """
        try:
            if not self._is_connected or self.llm is None:
                if not self.connect():
                    raise ConnectionError("Unable to establish connection to Ollama server")

            # Double-check llm is not None after connection
            if self.llm is None:
                raise ConnectionError("LLM instance is None after connection")

            response: BaseMessage = self.llm.invoke(input=message)

            # Handle different types of response content
            if isinstance(response.content, str):
                return response.content
            else:
                # Convert other types to string
                return str(response.content) if response.content is not None else None

        except Exception as e:
            self.logger.error(f"Failed to invoke model: {e}")
            return None

    def disconnect(self) -> None:
        """Disconnect from the Ollama server and clean up resources."""
        self.llm = None
        self._is_connected = False
        self.logger.info("Disconnected from Ollama server")

    def is_connected(self) -> bool:
        """
        Check if currently connected to the Ollama server.

        Returns:
            True if connected, False otherwise
        """
        return self._is_connected and self.llm is not None

    def update_config(
        self,
        model: Optional[str] = None,
        base_url: Optional[str] = None,
        temperature: Optional[float] = None,
    ) -> bool:
        """
        Update configuration and reconnect if necessary.

        Args:
            model: New model name (optional)
            base_url: New base URL (optional)
            temperature: New temperature setting (optional)
            timeout: New timeout setting (optional)

        Returns:
            True if update and reconnection successful, False otherwise
        """
        try:
            # Disconnect first
            self.disconnect()

            # Update configuration
            if model is not None:
                self.model = model
            if base_url is not None:
                self.base_url = base_url
            if temperature is not None:
                self.temperature = temperature

            # Reconnect with new configuration
            return self.connect()

        except Exception as e:
            self.logger.error(f"Failed to update configuration: {e}")
            return False

    @classmethod
    def reset_instance(cls) -> None:
        """Reset the singleton instance (useful for testing)."""
        if cls._instance:
            cls._instance.disconnect()
        cls._instance = None

    def __enter__(self) -> Self:
        """Context manager entry."""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Context manager exit with cleanup."""
        self.disconnect()

    def __repr__(self) -> str:
        """String representation of the Llama3 instance."""
        return f"Llama3(model='{self.model}', base_url='{self.base_url}', connected={self._is_connected})"
