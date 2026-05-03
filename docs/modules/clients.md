# :material-robot-outline: LLM Clients (`maticlib.llm`)

A universal interface for interacting with diverse LLM providers while maintaining common request/response schemas.

### **Initialization**

Each client is provider-specific but follows a shared constructor pattern.

```python
from maticlib.llm.openai import OpenAIClient
from maticlib.llm.google_genai import GoogleGenAIClient
from maticlib.llm.mistral import MistralClient

# OpenAI (Responses API)
oa_client = OpenAIClient(model="gpt-4o", api_key="sk-...", verbose=True)

# Google Gemini
gemini_client = GoogleGenAIClient(model="gemini-2.5-flash", thinking_budget=0)

# Mistral AI
mistral_client = MistralClient(model="mistral-large-latest")
```

### **Universal Methods**

- **`complete(input, response_model=None)`**: Synchronous completion.
    - **Input**: `str` or `List[BaseMessage]`.
    - **Output**: `LLMResponseBase` (see below).
- **`async_complete(input, response_model=None)`**: Asynchronous completion.
- **`get_text_response(response)`**: Helper to extract the primary text string from a response object.

### **The Response Object (`LLMResponseBase`)**

All clients return a standardized response object with these key fields:

- `content` (`str`): The primary generated text.
- `total_tokens` (`int`): Total count of prompt + completion tokens.
- `finish_reason` (`str`): Why the generation stopped (e.g., `stop`, `length`).
- `parsed_output` (`Any`): Contains the validated Pydantic model if a `response_model` was used.
