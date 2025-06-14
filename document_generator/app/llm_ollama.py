from langchain_core.messages.base import BaseMessage
from langchain_core.prompt_values import PromptValue
from langchain_ollama import ChatOllama


class Ollama:
    def __init__(self, model_name: str, url: str):
        """
        Initialize the Ollama client with the specified model and URL.

        Args:
            model_name (str): The name of the Ollama model to use.
            url (str): The base URL for the Ollama API.
        """
        self.model_name: str = model_name
        self.url: str = url
        self.client = ChatOllama(
            model=model_name,
            base_url=url,
            temperature=0.1,
        )

    def generate_response(
        self,
        prompt: PromptValue,
    ) -> BaseMessage:
        """
        Generate a response from the Ollama model based on the provided prompt.

        Args:
            prompt (str): The input prompt for the model.

        Returns:
            str: The generated response from the model.
        """
        client = ChatOllama(
            model=self.model_name,
            base_url=self.url,
            temperature=0.1,
        )
        return client.invoke(prompt)
