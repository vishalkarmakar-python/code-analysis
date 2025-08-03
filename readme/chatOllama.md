# ChatOllama Class Documentation

A comprehensive guide to the ChatOllama class from the `langchain_ollama` module for running open-source large language models locally with LangChain.

## Table of Contents

- [Overview](#overview)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Classes](#classes)
- [Initialization Parameters](#initialization-parameters)
- [Core Methods](#core-methods)
- [Inherited Methods](#inherited-methods)
- [Utility Functions](#utility-functions)
- [Features](#features)
- [Usage Examples](#usage-examples)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)

## Overview

ChatOllama is an Ollama chat model integration that allows you to run open-source large language models locally. It extends `BaseChatModel` and implements the standard `Runnable Interface`, providing seamless integration with LangChain applications.

### Key Benefits

- 🏠 **Local Execution**: Run models entirely on your machine
- 🔧 **Easy Integration**: Drop-in replacement for other LangChain chat models
- 🚀 **High Performance**: Optimized for local inference
- 🛠️ **Tool Support**: Native tool calling capabilities
- 📊 **Multi-modal**: Support for text and image inputs
- 🔄 **Streaming**: Real-time response generation

## Installation

```bash
# Install langchain-ollama
pip install -U langchain-ollama

# Install and setup Ollama
# macOS
brew install ollama
brew services start ollama

# Linux/WSL
curl -fsSL https://ollama.ai/install.sh | sh

# Download a model
ollama pull llama3.1
```

## Quick Start

```python
from langchain_ollama import ChatOllama

# Basic usage
llm = ChatOllama(model="llama3.1", temperature=0.7)
response = llm.invoke("Hello, how are you?")
print(response.content)

# With messages
messages = [
    ("system", "You are a helpful assistant."),
    ("human", "Explain machine learning in simple terms.")
]
response = llm.invoke(messages)
```

## Classes

| Class             | Module                                       | Description                                  | Inheritance                     |
| ----------------- | -------------------------------------------- | -------------------------------------------- | ------------------------------- |
| **ChatOllama**    | `langchain_ollama.chat_models`               | Main class for Ollama chat model integration | `BaseChatModel`                 |
| **BaseChatModel** | `langchain_core.language_models.chat_models` | Base class for chat models                   | `BaseLanguageModel`, `Runnable` |
| **AIMessage**     | `langchain_core.messages`                    | Response message from AI model               | `BaseMessage`                   |
| **HumanMessage**  | `langchain_core.messages`                    | Human input message                          | `BaseMessage`                   |
| **SystemMessage** | `langchain_core.messages`                    | System instruction message                   | `BaseMessage`                   |
| **ChatMessage**   | `langchain_core.messages`                    | Generic chat message with custom role        | `BaseMessage`                   |
| **ToolMessage**   | `langchain_core.messages`                    | Tool execution result message                | `BaseMessage`                   |

## Initialization Parameters

### Required Parameters

| Parameter | Type  | Required | Description                                              |
| --------- | ----- | -------- | -------------------------------------------------------- |
| **model** | `str` | ✅       | Name of Ollama model to use (e.g., "llama3.1", "gemma2") |

### Core Configuration

| Parameter       | Type              | Default                    | Description                                            |
| --------------- | ----------------- | -------------------------- | ------------------------------------------------------ |
| **temperature** | `float`           | `0.8`                      | Sampling temperature (0.0-1.0). Higher = more creative |
| **base_url**    | `str`             | `"http://localhost:11434"` | Ollama server URL                                      |
| **num_predict** | `int`             | `None`                     | Maximum number of tokens to generate                   |
| **format**      | `str`             | `None`                     | Output format ("json" for JSON responses)              |
| **keep_alive**  | `Union[int, str]` | `None`                     | How long to keep model in memory                       |

### Advanced Sampling Parameters

| Parameter          | Type        | Default | Description                               |
| ------------------ | ----------- | ------- | ----------------------------------------- |
| **top_k**          | `int`       | `40`    | Limits token selection to top K tokens    |
| **top_p**          | `float`     | `0.9`   | Nucleus sampling threshold                |
| **repeat_penalty** | `float`     | `1.1`   | Penalty for token repetition              |
| **repeat_last_n**  | `int`       | `64`    | Tokens to consider for repetition penalty |
| **seed**           | `int`       | `None`  | Random seed for reproducible output       |
| **stop**           | `List[str]` | `None`  | Stop sequences to end generation          |
| **tfs_z**          | `float`     | `1.0`   | Tail free sampling parameter              |

### Mirostat Parameters

| Parameter        | Type    | Default | Description                                     |
| ---------------- | ------- | ------- | ----------------------------------------------- |
| **mirostat**     | `int`   | `0`     | Mirostat sampling mode (0=disabled, 1=v1, 2=v2) |
| **mirostat_eta** | `float` | `0.1`   | Learning rate for Mirostat                      |
| **mirostat_tau** | `float` | `5.0`   | Target entropy for Mirostat                     |

### System Parameters

| Parameter      | Type  | Default | Description                 |
| -------------- | ----- | ------- | --------------------------- |
| **num_ctx**    | `int` | `2048`  | Context window size         |
| **num_gpu**    | `int` | `None`  | Number of GPU layers to use |
| **num_thread** | `int` | `None`  | Number of CPU threads       |

### LangChain Integration

| Parameter             | Type                                   | Default | Description                          |
| --------------------- | -------------------------------------- | ------- | ------------------------------------ |
| **cache**             | `Union[BaseCache, bool, None]`         | `None`  | Response caching configuration       |
| **callbacks**         | `Callbacks`                            | `None`  | Callback handlers for tracing        |
| **metadata**          | `Dict[str, Any]`                       | `None`  | Metadata for run tracing             |
| **tags**              | `List[str]`                            | `None`  | Tags for run categorization          |
| **rate_limiter**      | `BaseRateLimiter`                      | `None`  | Rate limiting configuration          |
| **disable_streaming** | `Union[bool, Literal['tool_calling']]` | `False` | Disable streaming for specific cases |

### HTTP Configuration

| Parameter               | Type             | Default | Description                     |
| ----------------------- | ---------------- | ------- | ------------------------------- |
| **headers**             | `Dict[str, str]` | `None`  | Additional HTTP headers         |
| **client_kwargs**       | `Dict[str, Any]` | `None`  | HTTP client configuration       |
| **async_client_kwargs** | `Dict[str, Any]` | `None`  | Async HTTP client configuration |

## Core Methods

### Primary Interaction Methods

| Method      | Parameters                                                                                                               | Return Type   | Description                                  |
| ----------- | ------------------------------------------------------------------------------------------------------------------------ | ------------- | -------------------------------------------- |
| **invoke**  | `input: LanguageModelInput, config: Optional[RunnableConfig] = None, *, stop: Optional[List[str]] = None, **kwargs: Any` | `BaseMessage` | Primary method for single message generation |
| **ainvoke** | `input: LanguageModelInput, config: Optional[RunnableConfig] = None, *, stop: Optional[List[str]] = None, **kwargs: Any` | `BaseMessage` | Async version of invoke                      |

### Streaming Methods

| Method      | Parameters                                                                                                               | Return Type                       | Description                         |
| ----------- | ------------------------------------------------------------------------------------------------------------------------ | --------------------------------- | ----------------------------------- |
| **stream**  | `input: LanguageModelInput, config: Optional[RunnableConfig] = None, *, stop: Optional[List[str]] = None, **kwargs: Any` | `Iterator[BaseMessageChunk]`      | Stream response chunks in real-time |
| **astream** | `input: LanguageModelInput, config: Optional[RunnableConfig] = None, *, stop: Optional[List[str]] = None, **kwargs: Any` | `AsyncIterator[BaseMessageChunk]` | Async streaming                     |

### Batch Processing Methods

| Method                  | Parameters                                                                                                                                             | Return Type                                           | Description                         |
| ----------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------- | ----------------------------------- |
| **batch**               | `inputs: List[Input], config: Optional[Union[RunnableConfig, List[RunnableConfig]]] = None, *, return_exceptions: bool = False, **kwargs: Any`         | `List[Output]`                                        | Process multiple inputs in batch    |
| **abatch**              | `inputs: Sequence[Input], config: Optional[Union[RunnableConfig, Sequence[RunnableConfig]]] = None, *, return_exceptions: bool = False, **kwargs: Any` | `List[Output]`                                        | Async batch processing              |
| **batch_as_completed**  | `inputs: Sequence[Input], config: Optional[Union[RunnableConfig, Sequence[RunnableConfig]]] = None, *, return_exceptions: bool = False, **kwargs: Any` | `Iterator[Tuple[int, Union[Output, Exception]]]`      | Process batch with completion order |
| **abatch_as_completed** | `inputs: Sequence[Input], config: Optional[Union[RunnableConfig, Sequence[RunnableConfig]]] = None, *, return_exceptions: bool = False, **kwargs: Any` | `AsyncIterator[Tuple[int, Union[Output, Exception]]]` | Async batch with completion order   |

### Generation Methods

| Method        | Parameters                                                                                                                                                                                                                                  | Return Type | Description                                   |
| ------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------- | --------------------------------------------- |
| **generate**  | `messages: List[List[BaseMessage]], stop: Optional[List[str]] = None, callbacks: Optional[Callbacks] = None, *, tags: Optional[List[str]] = None, metadata: Optional[Dict[str, Any]] = None, run_name: Optional[str] = None, **kwargs: Any` | `LLMResult` | Generate responses for multiple message lists |
| **agenerate** | `messages: List[List[BaseMessage]], stop: Optional[List[str]] = None, callbacks: Optional[Callbacks] = None, *, tags: Optional[List[str]] = None, metadata: Optional[Dict[str, Any]] = None, run_name: Optional[str] = None, **kwargs: Any` | `LLMResult` | Async version of generate                     |

### Tool Integration Methods

| Method                     | Parameters                                                                                                                                                 | Return Type                                 | Description                           |
| -------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------- | ------------------------------------- |
| **bind_tools**             | `tools: Sequence[Union[Dict[str, Any], Type, Callable, BaseTool]], **kwargs: Any`                                                                          | `Runnable[LanguageModelInput, BaseMessage]` | Bind tools for function calling       |
| **with_structured_output** | `schema: Union[Dict, Type[BaseModel]], *, method: Literal["function_calling", "json_mode"] = "function_calling", include_raw: bool = False, **kwargs: Any` | `Runnable`                                  | Get structured output matching schema |

## Inherited Methods

### Runnable Interface Methods

| Method          | Parameters                                                                                                                                                             | Return Type                                | Description                          |
| --------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------ | ------------------------------------ |
| **bind**        | `**kwargs: Any`                                                                                                                                                        | `Runnable`                                 | Bind arguments to runnable           |
| **with_config** | `config: RunnableConfig`                                                                                                                                               | `Runnable`                                 | Bind configuration to runnable       |
| **with_types**  | `*, input_type: Optional[Type[Input]] = None, output_type: Optional[Type[Output]] = None`                                                                              | `Runnable[Input, Output]`                  | Add type information                 |
| **with_retry**  | `*, retry_if_exception_type: Tuple[Type[BaseException], ...] = (<class 'Exception'>,), wait_exponential_jitter: bool = True, stop_after_attempt: int = 3`              | `Runnable[Input, Output]`                  | Add retry logic                      |
| **assign**      | `**kwargs: Union[Runnable[Dict[str, Any], Any], Callable[[Dict[str, Any]], Any], Mapping[str, Union[Runnable[Dict[str, Any], Any], Callable[[Dict[str, Any]], Any]]]]` | `Runnable[Dict[str, Any], Dict[str, Any]]` | Assign additional keys to input dict |

### Configuration Methods

| Method                        | Parameters                                                                                                                                                              | Return Type                             | Description                         |
| ----------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------- | ----------------------------------- |
| **configurable_fields**       | `**kwargs: AnyConfigurableField`                                                                                                                                        | `RunnableSerializable[Input, Output]`   | Make fields configurable at runtime |
| **configurable_alternatives** | `which: ConfigurableField, *, default_key: str = "default", prefix_keys: bool = False, **kwargs: Union[Runnable[Input, Output], Callable[[], Runnable[Input, Output]]]` | `RunnableSerializable[Input, Output]`   | Configure alternative runnables     |
| **with_fallbacks**            | `fallbacks: Sequence[Runnable[Input, Output]], *, exceptions_to_handle: Tuple[Type[BaseException], ...] = (<class 'Exception'>,), exception_key: Optional[str] = None`  | `RunnableWithFallbacksT[Input, Output]` | Add fallback runnables              |

### Advanced Streaming Methods

| Method             | Parameters                                                                                                                                                                                                                                                                                                                                                                                                                   | Return Type                  | Description                          |
| ------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------- | ------------------------------------ |
| **astream_events** | `input: Input, config: Optional[RunnableConfig] = None, *, version: Literal["v1", "v2"], include_names: Optional[Sequence[str]] = None, include_types: Optional[Sequence[str]] = None, include_tags: Optional[Sequence[str]] = None, exclude_names: Optional[Sequence[str]] = None, exclude_types: Optional[Sequence[str]] = None, exclude_tags: Optional[Sequence[str]] = None, **kwargs: Any`                              | `AsyncIterator[StreamEvent]` | Stream events with detailed metadata |
| **astream_log**    | `input: Input, config: Optional[RunnableConfig] = None, *, diff: bool = True, with_streamed_output_list: bool = True, include_names: Optional[Sequence[str]] = None, include_types: Optional[Sequence[str]] = None, include_tags: Optional[Sequence[str]] = None, exclude_names: Optional[Sequence[str]] = None, exclude_types: Optional[Sequence[str]] = None, exclude_tags: Optional[Sequence[str]] = None, **kwargs: Any` | `AsyncIterator[RunLogPatch]` | Stream run logs                      |

### Composition Methods

| Method   | Parameters                            | Return Type                                   | Description                          |
| -------- | ------------------------------------- | --------------------------------------------- | ------------------------------------ |
| **pipe** | `*others, name: Optional[str] = None` | `RunnableSerializable`                        | Create pipeline with other runnables |
| **pick** | `keys: Union[str, List[str]]`         | `RunnableSerializable`                        | Pick specific keys from output       |
| **map**  | None                                  | `RunnableEachBase[List[Input], List[Output]]` | Map over list of inputs              |

## Utility Functions

### Token Management

| Function                         | Parameters                    | Return Type | Description                  |
| -------------------------------- | ----------------------------- | ----------- | ---------------------------- |
| **get_num_tokens**               | `text: str`                   | `int`       | Count tokens in text         |
| **get_num_tokens_from_messages** | `messages: List[BaseMessage]` | `int`       | Count tokens in message list |

### Model Information

| Function              | Parameters                                                    | Return Type       | Description         |
| --------------------- | ------------------------------------------------------------- | ----------------- | ------------------- |
| **get_graph**         | `config: Optional[RunnableConfig] = None`                     | `Graph`           | Get execution graph |
| **get_input_schema**  | `config: Optional[RunnableConfig] = None`                     | `Type[BaseModel]` | Get input schema    |
| **get_output_schema** | `config: Optional[RunnableConfig] = None`                     | `Type[BaseModel]` | Get output schema   |
| **get_name**          | `suffix: Optional[str] = None, *, name: Optional[str] = None` | `str`             | Get runnable name   |

### Lifecycle Management

| Function            | Parameters                                                                                                                      | Return Type               | Description                   |
| ------------------- | ------------------------------------------------------------------------------------------------------------------------------- | ------------------------- | ----------------------------- |
| **with_listeners**  | `*, on_start: Optional[Listener] = None, on_end: Optional[Listener] = None, on_error: Optional[Listener] = None`                | `Runnable[Input, Output]` | Add lifecycle listeners       |
| **awith_listeners** | `*, on_start: Optional[AsyncListener] = None, on_end: Optional[AsyncListener] = None, on_error: Optional[AsyncListener] = None` | `Runnable[Input, Output]` | Add async lifecycle listeners |

## Features

### 🛠️ Tool Calling

ChatOllama supports native tool calling for compatible models:

```python
from langchain_core.tools import tool
from langchain_ollama import ChatOllama

@tool
def get_weather(location: str) -> str:
    """Get weather for a location."""
    return f"Sunny, 72°F in {location}"

llm = ChatOllama(model="llama3.1").bind_tools([get_weather])
```

### 📊 Structured Output

Force the model to respond in a specific format:

```python
from pydantic import BaseModel, Field

class PersonInfo(BaseModel):
    name: str = Field(description="Person's name")
    age: int = Field(description="Person's age")

structured_llm = llm.with_structured_output(PersonInfo)
```

### 🎯 JSON Mode

Force JSON responses:

```python
json_llm = ChatOllama(model="llama3.1", format="json")
```

### 🖼️ Multi-modal Support

Process images with vision models:

```python
from langchain_core.messages import HumanMessage

llm = ChatOllama(model="llava")
message = HumanMessage(content=[
    {"type": "text", "text": "What's in this image?"},
    {"type": "image_url", "image_url": "data:image/jpeg;base64,{base64_image}"}
])
```

### 🚀 Streaming

Real-time response generation:

```python
for chunk in llm.stream("Tell me a story"):
    print(chunk.content, end="", flush=True)
```

### 🔄 Async Support

Full async/await support:

```python
async def chat():
    response = await llm.ainvoke("Hello!")
    return response
```

## Usage Examples

### Basic Chat

```python
from langchain_ollama import ChatOllama

llm = ChatOllama(model="llama3.1", temperature=0.7)

# Simple text
response = llm.invoke("What is machine learning?")
print(response.content)

# Conversation
messages = [
    ("system", "You are a helpful coding assistant."),
    ("human", "How do I reverse a string in Python?"),
]
response = llm.invoke(messages)
```

### Streaming Chat

```python
def streaming_chat():
    query = "Explain quantum computing step by step"
    print("AI: ", end="")

    for chunk in llm.stream(query):
        print(chunk.content, end="", flush=True)
    print()
```

### Tool Usage

```python
from langchain_core.tools import tool

@tool
def calculate(expression: str) -> str:
    """Calculate mathematical expressions safely."""
    try:
        return str(eval(expression))
    except:
        return "Invalid expression"

llm_with_tools = llm.bind_tools([calculate])
response = llm_with_tools.invoke("What is 25 * 4 + 10?")

if response.tool_calls:
    for tool_call in response.tool_calls:
        print(f"Tool: {tool_call['name']}")
        print(f"Args: {tool_call['args']}")
```

### Batch Processing

```python
inputs = [
    "Summarize: The key to success is persistence.",
    "Translate to French: Hello, how are you?",
    "Generate a haiku about technology"
]

responses = llm.batch(inputs)
for i, response in enumerate(responses):
    print(f"Input {i+1}: {response.content[:50]}...")
```

### Configuration Chain

```python
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_template(
    "You are a {role}. Answer this question: {question}"
)

chain = (
    prompt
    | llm.bind(temperature=0.9, max_tokens=100)
    | StrOutputParser()
)

result = chain.invoke({
    "role": "data scientist",
    "question": "What is feature engineering?"
})
```

### Error Handling with Fallbacks

```python
primary_llm = ChatOllama(model="llama3.1")
fallback_llm = ChatOllama(model="llama2")

robust_llm = primary_llm.with_fallbacks([fallback_llm])
response = robust_llm.invoke("Complex query here")
```

## Best Practices

### 🎯 Model Selection

| Model             | Use Case                        | Context Window | Performance |
| ----------------- | ------------------------------- | -------------- | ----------- |
| **llama3.1:8b**   | General purpose, balanced       | 128K           | High        |
| **llama3.1:70b**  | Complex reasoning, high quality | 128K           | Very High   |
| **gemma2:9b**     | Fast inference, efficiency      | 8K             | High        |
| **codellama:13b** | Code generation and analysis    | 16K            | High        |
| **llava:13b**     | Multi-modal (text + images)     | 4K             | Medium      |

### ⚡ Performance Optimization

```python
# Optimal configuration for production
llm = ChatOllama(
    model="llama3.1:8b",
    temperature=0.1,          # Lower for consistency
    num_predict=512,          # Limit output length
    num_ctx=4096,            # Reasonable context size
    num_thread=8,            # Match CPU cores
    keep_alive="10m",        # Keep model loaded
    cache=True               # Enable caching
)
```

### 🔒 Error Handling

```python
from langchain_core.exceptions import LangChainException

try:
    response = llm.invoke("Your query here")
except LangChainException as e:
    print(f"LangChain error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

### 📏 Token Management

```python
def check_token_limit(llm, text, max_tokens=4000):
    """Ensure text fits within token limits."""
    tokens = llm.get_num_tokens(text)
    if tokens > max_tokens:
        print(f"⚠️ Text too long: {tokens} tokens (max: {max_tokens})")
        return False
    return True

# Check before processing
if check_token_limit(llm, user_input):
    response = llm.invoke(user_input)
```

## Troubleshooting

### Common Issues

| Issue                  | Cause                | Solution                                  |
| ---------------------- | -------------------- | ----------------------------------------- |
| **Connection refused** | Ollama not running   | Start Ollama: `ollama serve`              |
| **Model not found**    | Model not downloaded | Download: `ollama pull model_name`        |
| **Out of memory**      | Model too large      | Use smaller model or increase RAM         |
| **Slow responses**     | CPU/GPU limitations  | Optimize `num_thread`, `num_gpu`          |
| **Empty responses**    | Context too long     | Reduce input length or increase `num_ctx` |

### Debug Configuration

```python
# Enable verbose logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Add callbacks for debugging
from langchain.callbacks import StdOutCallbackHandler

llm = ChatOllama(
    model="llama3.1",
    callbacks=[StdOutCallbackHandler()],
    verbose=True
)
```

### Health Check

```python
def health_check():
    """Check if Ollama is responding correctly."""
    try:
        llm = ChatOllama(model="llama3.1")
        response = llm.invoke("Hello")
        print("✅ Ollama is working correctly")
        return True
    except Exception as e:
        print(f"❌ Ollama error: {e}")
        return False

health_check()
```

---

## Contributing

Contributions are welcome! Please read the contributing guidelines and submit pull requests for any improvements.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

- 📖 [LangChain Documentation](https://python.langchain.com/docs/)
- 🦙 [Ollama Documentation](https://ollama.ai/docs)
- 💬 [LangChain Discord](https://discord.gg/langchain)
- 🐛 [Issue Tracker](https://github.com/langchain-ai/langchain/issues)
