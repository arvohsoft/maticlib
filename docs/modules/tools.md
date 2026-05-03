# :material-hammer-wrench: Tools (`maticlib.tools`)

The Tools module enables LLMs to execute external Python functions by automatically generating the necessary JSON Schemas for provider-specific "Function Calling" features.

### **Imports**
```python
from maticlib.tools import tool
```

### **How it Works**
Maticlib uses **introspection** to minimize boilerplate. When you apply the `@tool` decorator, it inspects your function to build a metadata object:

| Component | Source | Outcome |
| :--- | :--- | :--- |
| **Name** | `func.__name__` | Identified as the tool name for the LLM. |
| **Description** | `docstring` | Provided as instructions to the LLM on *when* to use the tool. |
| **Parameters** | `type hints` | Converted to JSON Schema types (string, integer, etc.). |
| **Required Fields** | `signature` | Parameters without default values are marked as `required`. |

### **Guided Example**

This example demonstrates defining a tool with specific type hints and using it with an asynchronous client.

```python
from maticlib.tools import tool
from maticlib.llm.openai import OpenAIClient

# 1. Define your tool with type hints and a clear docstring
@tool
def calculate_itinerary(destination: str, days: int = 3):
    """
    Generates a travel itinerary for a specific destination and duration.
    """
    return f"A {days}-day trip to {destination} is planned."

# 2. Use it with any client
client = OpenAIClient()

async def main():
    response = await client.async_complete(
        input="I want a 5-day trip to Tokyo",
        tools=[calculate_itinerary]
    )

    # 3. Check for tool requests
    if response.tool_calls:
        for call in response.tool_calls:
            print(f"Model wants to call: {call['function']['name']}")
            print(f"With arguments: {call['function']['arguments']}")

# The extracted schema is stored on the function itself
print(calculate_itinerary.matic_tool_metadata)
```

### **Provider Support**

The native tool calling system is optimized for these provider-specific schemas:

| Provider | Schema / Feature | Implementation Details |
| :--- | :--- | :--- |
| **OpenAI** | `/v1/responses` | Uses the modern Response API with `tool_calls`. |
| **Google Gemini** | `function_declarations` | Maps Python signatures to Gemini's native declarations. |
| **Mistral AI** | `tools` array | Implements core tool schema for chat completions. |
