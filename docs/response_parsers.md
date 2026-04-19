# Response Parsers

Maticlib provides a powerful system for extracting structured data from LLM responses. This allows you to go beyond simple text strings and receive fully-validated Python objects (Pydantic models), JSON dictionaries, or XML-based data.

## :material-rocket-launch-outline: Pydantic Response Parser (Recommended)

The easiest and most robust way to get structured data is by passing a Pydantic model directly to the client's `complete()` method via the `response_model` parameter.

### Example

```python
from pydantic import BaseModel, Field
from maticlib.llm.openai import OpenAIClient

# 1. Define your structure
class UserProfile(BaseModel):
    username: str
    email: str
    age: int = Field(..., gt=0)
    interests: list[str]

client = OpenAIClient()

# 2. Pass the model to complete()
response = client.complete(
    "Generate a profile for a tech enthusiast.",
    response_model=UserProfile
)

# 3. Access validated data
profile = response.parsed_output
print(f"User: {profile.username}, Age: {profile.age}")
```

### How it works
When you provide a `response_model`:
1.  **Instruction Injection**: Maticlib automatically appends JSON schema instructions to your prompt.
2.  **Robust Extraction**: It uses regex to find JSON blocks even if the LLM adds conversational filler.
3.  **Validation**: It validates the extracted JSON against your Pydantic model. If validation fails, `parsed_output` will be `None` and a warning will be logged.

---

## :material-package-variant-closed: JSON Response Parser

If you don't need the strict validation of Pydantic and just want a dictionary:

```python
from maticlib.core.parsers.json import JSONResponseParser

parser = JSONResponseParser()
text = "Result: ```json\n{'key': 'value'}\n```"
data = parser.parse(text)
# data = {'key': 'value'}
```

*Note: The clients currently prioritize Pydantic models for the `response_model` parameter. Manual use of `JSONResponseParser` is useful for custom workflows.*

---

## :material-tree-outline: XML Response Parser

For legacy systems or specific prompting techniques, you can use XML-based extraction:

```python
from maticlib.core.parsers.xml import XMLResponseParser

parser = XMLResponseParser()
text = "<data><id>123</id><status>active</status></data>"
data = parser.parse(text)
# data = {'id': '123', 'status': 'active'}
```

It extracts tags and their text content into a flat dictionary. If nested tags are found, it focuses on the children of the first detected root-like element.

---

## :material-tools: Implementation Details

All parsers inherit from `BaseResponseParser` and implement two key methods:
- `parse(text: str)`: The logic to convert text into a structured object.
- `get_structure_instructions()`: The string to be injected into the LLM prompt to guide its formatting.
