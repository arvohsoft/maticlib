# :material-code-json: Response Parsers (`maticlib.core.parsers`)

Advanced utilities to force LLMs into generating structured, machine-readable data.

### **Available Parsers**

1. **`PydanticResponseParser`**: (Recommended) Validates against a Pydantic `BaseModel`.
2. **`JSONResponseParser`**: Extracts a raw Python dictionary from JSON blocks.
3. **`XMLResponseParser`**: Extracts data from flat XML tags.

### **Integration Workflow**

You don't need to call the parser manually. Simply pass your model to the client.

```python
from pydantic import BaseModel
from maticlib.llm.openai import OpenAIClient

class Sentiment(BaseModel):
    score: float
    label: str

client = OpenAIClient()

# Maticlib automatically injects formatting instructions and parses the result
response = client.complete(
    input="Analyze this: I love structural documentation!",
    response_model=Sentiment
)

# Access the validated Pydantic object directly
sentiment = response.parsed_output
print(f"{sentiment.label}: {sentiment.score}")
```
