# Release Notes

Stay up to date with the latest features, improvements, and bug fixes in Maticlib.

---

## :material-tag-outline: [v0.1.6] - 2026-04-17
 
### :material-sparkles: Major Additions
 
#### **Response Parser System**
A new, LangChain-inspired structured output system. Developers can now pass a Pydantic `BaseModel` directly to any LLM client to receive validated, type-safe Python objects.
- `PydanticResponseParser`: Auto-generates structural instructions and validates output.
- `JSONResponseParser`: Robust regex-based dictionary extraction.
- `XMLResponseParser`: Flat dictionary extraction from XML tags.

### :material-wrench-outline: Fixes & Improvements
- **LLM Clients**: Updated default Gemini model to `gemini-2.5-lite`.
- **API Key Detection**: Fixed a race condition where environment variables were not picked up correctly at import time.
- **MRO Fixes**: Resolved method resolution order conflicts in the parser inheritance hierarchy.

---

## :material-tag-outline: [v0.1.5] - 2026-04-12

### :material-sparkles: Major Additions

#### **OpenAI Integration**
We've added a robust `OpenAIClient` that leverages the modern **Responses API**. This ensures compatibility with the latest reasoning models (o-series) and provides detailed metadata like cached tokens.

#### **Automated Documentation**
The library now features a professional documentation site built with MkDocs. This includes an automated API reference that stays in sync with the source code.

#### **Comprehensive Examples**
A new `examples/` directory has been populated with scripts covering everything from basic chat to complex parallel execution graphs.

### :material-wrench-outline: Fixes & Improvements
- **MaticGraph**: Fixed a critical constructor assignment bug and resolved Unicode encoding issues on Windows.
- **LLM Clients**: Better API key validation and improved fallback logic for Gemini.
- **Aesthetics**: Replaced library-wide emojis with clean, professional Material Design icons.

---

## :material-tag-outline: [v0.1.4] - 2025-10-24

### :material-plus: Added
- **Parallel execution support in MaticGraph**: Explicit fan-out/fan-in patterns using the `parallel_group()` method.
- **System instruction support**: Properly formatted system instructions for Google Gemini models.

### :material-arrow-up-circle-outline: Changed
- **Async Client Management**: Better resource cleanup and timeout handling in asynchronous requests.

---

*For full historical details, please consult the [CHANGELOG.md](https://github.com/arvohsoft/maticlib/blob/main/CHANGELOG.md) in the repository.*
