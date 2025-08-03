from contextlib import contextmanager
from dotenv import load_dotenv
from langchain_core.messages.base import BaseMessage
from langchain_ollama import ChatOllama
from os import getenv
from tiktoken import Encoding, get_encoding
from typing import Any, ClassVar, Dict, Generator, List, Literal, Optional, Self


class Ollama:
    _instance: ClassVar[Self | None] = None
    _model_name: ClassVar[str | None] = None  # Track which model was initialized

    def __new__(cls, model_name: str) -> Self:
        if cls._instance is None:
            cls._instance = super(Ollama, cls).__new__(cls)
            cls._model_name = model_name
        elif cls._model_name != model_name:
            # Print warning about model name mismatch in singleton
            print(
                f"[WARNING] Ollama singleton already initialized with model '{cls._model_name}'. "
                f"Ignoring new model name '{model_name}'. Use separate instances if needed."
            )
        return cls._instance

    def __init__(self, model_name: str) -> None:
        if not hasattr(self, "_initialized"):
            # Set up model identifier for debugging and error tracking
            self._model_identifier: str = model_name

            # Initialize state flags
            self._initialized: bool = False
            self._is_connected: bool = False

            try:
                # Load and validate environment variables
                if self._load_environment_variables(model_name=model_name):
                    # Extract configuration from loaded environment variables
                    self._model: str = self._config[f"OLLAMA_MODEL_{model_name}"]
                    self._model_max_tokens: int = self._config[f"OLLAMA_MODEL_{model_name}_MAX_TOKENS"]
                    self._model_max_chunk: int = self._config[f"OLLAMA_MODEL_{model_name}_MAX_CHUNK"]
                    self._model_max_gpu: float = self._config["OLLAMA_GPU"]
                    self._model_base_url: str = self._config["OLLAMA_MODEL_BASE_URL"]
                    self._model_temperature: float = self._config["OLLAMA_MODEL_TEMPERATURE"]

                    # Create the ChatOllama instance with loaded configuration
                    self._llm: ChatOllama = self._create_llm_instance()

                    # Test the connection to ensure model is accessible
                    self._is_connected = self._test_connection()

                    # Mark as successfully initialized
                    self._initialized = True
                    print(f"[INFO] Ollama initialized successfully with model: {self._model}")
                else:
                    raise RuntimeError("Failed to load required environment variables")

            except Exception as error:
                print(f"[ERROR] Ollama initialization failed: {str(error)}")
                raise

    @classmethod
    def ensure_instance(cls, model_name: str) -> Self:
        """
        Ensure a singleton instance exists with the specified model.
        Creates if doesn't exist, warns if different model exists.

        Args:
            model_name: Model name to ensure

        Returns:
            Self: The singleton instance

        Usage:
            ollama = Ollama.ensure_instance("llama3")  # Creates or gets existing
        """
        if cls._instance is None:
            print(f"[INFO] Creating new Ollama instance with model: {model_name}")
            return cls(model_name)
        elif cls._model_name != model_name:
            print(f"[WARNING] Requested model '{model_name}' differs from existing '{cls._model_name}'")
            return cls._instance
        else:
            print(f"[INFO] Using existing Ollama instance with model: {model_name}")
            return cls._instance

    @classmethod
    def get_instance(cls) -> Optional[Self]:
        """
        Get the current singleton instance without creating a new one.

        Returns:
            Optional[Self]: Current instance if exists, None otherwise

        Usage:
            current_ollama = Ollama.get_instance()
            if current_ollama:
                # Use existing instance
                pass
        """
        return cls._instance

    @classmethod
    def destroy_instance(cls) -> bool:
        """
        Destroy the singleton instance and cleanup resources.

        Returns:
            bool: True if instance was destroyed, False if no instance existed
        """
        if cls._instance is not None:
            try:
                # Cleanup instance resources if they exist
                if hasattr(cls._instance, "_llm") and cls._instance._llm is not None:
                    print("[DEBUG] Cleaning up LLM instance")

                # Clear instance variables
                if hasattr(cls._instance, "_config"):
                    cls._instance._config.clear()

                # Print the destruction info
                model_name: Any | str = getattr(cls._instance, "_model", "unknown")
                print(f"[INFO] Destroying Ollama singleton instance for model: {model_name}")

                # Reset class variables
                cls._instance = None
                cls._model_name = None

                print("[DEBUG] Ollama singleton instance destroyed successfully")
                return True

            except Exception as error:
                print(f"[ERROR] Error during singleton destruction: {str(error)}")
                # Still reset the instance even if cleanup failed
                cls._instance = None
                cls._model_name = None
                return True
        else:
            return False

    @classmethod
    def instance_exists(cls) -> bool:
        """
        Check if a singleton instance currently exists.

        Returns:
            bool: True if instance exists, False otherwise

        Usage:
            if Ollama.instance_exists():
                print("Ollama is already running")
        """
        return cls._instance is not None

    @classmethod
    def get_current_model_name(cls) -> Optional[str]:
        """
        Get the model name of the current singleton instance.

        Returns:
            Optional[str]: Model name if instance exists, None otherwise

        Usage:
            model = Ollama.get_current_model_name()
            print(f"Current model: {model}")
        """
        return cls._model_name

    @classmethod
    def get_status(cls) -> Dict[str, Any]:
        """
        Get comprehensive status information about the singleton.

        Returns:
            Dict[str, Any]: Status information including existence, initialization, model, etc.

        Usage:
            status = Ollama.get_status()
            print(f"Status: {status}")
        """
        if cls._instance is None:
            return {"exists": False, "initialized": False, "model_name": None, "connected": False, "base_url": None, "temperature": None}

        return {
            "exists": True,
            "initialized": getattr(cls._instance, "_initialized", False),
            "model_name": cls._model_name,
            "connected": getattr(cls._instance, "_is_connected", False),
            "base_url": getattr(cls._instance, "_model_base_url", None),
            "temperature": getattr(cls._instance, "_model_temperature", None),
        }

    def _load_environment_variables(self, model_name: str) -> bool:
        """Instance method - operates on self._config"""
        self._config: Dict[str, Any] = {}

        # Define required environment variable names
        required_vars: List[str] = [
            f"OLLAMA_MODEL_{model_name}",
            f"OLLAMA_MODEL_{model_name}_MAX_TOKENS",
            f"OLLAMA_MODEL_{model_name}_MAX_CHUNK",
            "OLLAMA_MODEL_BASE_URL",
            "OLLAMA_MODEL_TEMPERATURE",
            "OLLAMA_GPU",
        ]

        try:
            # Attempt to load environment variables from .env file
            if not load_dotenv():
                print("[ERROR] Failed to load environment variables from .env file")
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

            print(f"[DEBUG] Successfully loaded {len(required_vars)} environment variables")
            return True

        except Exception as error:
            print(f"[ERROR] Environment variable loading failed: {str(error)}")
            raise

    def _create_llm_instance(self) -> ChatOllama:
        """Instance method - uses self._model, self._base_url, etc."""
        try:
            # Create ChatOllama instance with loaded configuration
            llm_instance = ChatOllama(
                model=self._model,  # Model name (e.g., "llama3.1:8b")
                base_url=self._model_base_url,  # Ollama service URL
                temperature=self._model_temperature,  # Response randomness (0.0-2.0)
                # Enhanced parameters for better performance:
                num_ctx=int(self._model_max_tokens),  # Context window size (16K tokens)
                num_gpu=int(self._model_max_gpu),  # Context window size (16K tokens)
                num_predict=int(self._model_max_tokens),  # Maximum tokens to generate
                top_k=1,  # Top-k sampling
                top_p=0.1,  # Top-p sampling
                # num_ctx=16384,  # Context window size (16K tokens)
                # num_predict=4096,  # Maximum tokens to generate
            )

            print(f"[DEBUG] ChatOllama instance created successfully for model: {self._model}")
            return llm_instance

        except Exception as error:
            print(f"[ERROR] Failed to create ChatOllama instance: {error}")
            raise

    def _test_connection(self) -> bool:
        """Instance method - uses self._llm"""
        # Ensure LLM instance exists before testing
        assert self._llm is not None, "Ollama model is not initialized"

        try:
            # Send a simple test message to verify connectivity
            test_message: str = "Hello, this is a connection test."
            response: BaseMessage = self._llm.invoke(input=test_message)

            # Validate that we received a proper response
            if response and response.content:
                print("[INFO] Model connection test successful")

                # Print response preview for debugging (first 100 characters)
                if isinstance(response.content, str):
                    preview: str = response.content[:100]
                    print(f"[DEBUG] Test response preview: {preview}...")

                return True
            else:
                print("[WARNING] Model connection test returned empty response")
                return False

        except Exception as error:
            print(f"[ERROR] Model connection test failed: {str(error)}")
            return False

    def get_token_count(self, content: str) -> int:
        """Instance method - uses self._llm and self._initialized"""
        if not self._initialized:
            raise RuntimeError("LLM not initialized")
        return self._llm.get_num_tokens(text=content)

    @staticmethod
    def count_tokens(content: str) -> int:
        """Instance method - uses self._llm and self._initialized"""
        try:
            encoding: Encoding = get_encoding("cl100k_base")
            return len(encoding.encode(content))
        except Exception as error:
            print(f"[ERROR] Tiktoken counting failed: {error}")
            # Fallback to a simple character count if tiktoken fails
            return len(content)

    @contextmanager
    def get_llm(self) -> Generator[ChatOllama, None, None]:
        """Instance method - uses self._llm and self._initialized"""
        # Ensure LLM is properly initialized before yielding
        if not self._initialized or not hasattr(self, "_llm"):
            raise Exception("LLM not initialized. Check initialization status.")

        try:
            # Yield the ChatOllama instance for use
            yield self._llm
        except Exception as error:
            # Print any errors that occur during LLM operations
            print(f"[ERROR] LLM operation error: {str(error)}")
            raise

    def __enter__(self) -> Self:
        """Instance method - context manager protocol"""
        if not self._initialized:
            raise Exception("LLM not initialized. Check initialization status.")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Instance method - context manager protocol"""
        if exc_type is not None:
            # Print any exceptions that occurred in the context
            print(f"[ERROR] Exception occurred in Ollama context: {exc_type.__name__}: {exc_val}")
        # Return None to allow exceptions to propagate normally
        return None

    def __del__(self) -> None:
        """Instance method - destructor must be instance method"""
        try:
            if hasattr(self, "_model"):
                print(f"[DEBUG] Ollama instance for model '{self._model}' is being garbage collected")
        except:
            # Ignore any errors during destruction
            pass

    @property
    def is_initialized(self) -> bool:
        """Instance property - checks self._initialized"""
        return getattr(self, "_initialized", False)

    @property
    def get_llm_instance(self) -> ChatOllama:
        """Instance property - returns self._llm"""
        if not getattr(self, "_initialized", False):
            raise RuntimeError("LLM instance is not initialized. Ensure the Ollama class was properly instantiated with valid configuration.")

        if not hasattr(self, "_llm"):
            raise RuntimeError("LLM instance is missing. This indicates an initialization error.")

        return self._llm

    @property
    def connection_exists(self) -> bool:
        """Instance property - checks self._is_connected"""
        return getattr(self, "_is_connected", False)

    @property
    def model_name(self) -> Optional[str]:
        """Instance property - returns self._model"""
        return getattr(self, "_model", None)

    @property
    def model_max_token(self) -> int:
        """Instance property - returns self._model_max_tokens"""
        return int(getattr(self, "_model_max_tokens", 0))

    @property
    def model_max_gpu(self) -> Optional[str]:
        """Instance property - returns self._model_max_gpu"""
        return getattr(self, "_model_max_gpu", None)

    @property
    def model_base_url(self) -> Optional[str]:
        """Instance property - returns self._base_url"""
        return getattr(self, "_model_base_url", None)

    @property
    def temperature(self) -> Optional[float]:
        """Instance property - returns self._temperature"""
        return getattr(self, "_temperature", None)

    @property
    def model_identifier(self) -> Optional[str]:
        """Instance property - returns self._model_identifier"""
        return getattr(self, "_model_identifier", None)

    def __repr__(self) -> str:
        """Instance method - accesses instance state"""
        status: Literal["initialized"] | Literal["not initialized"] = "initialized" if self.is_initialized else "not initialized"
        model: str = self.model_name or "unknown"
        return f"Ollama(model='{model}', status='{status}')"
