# Maticlib

**A Python Automation Library for creating intelligent AI agents**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Downloads](https://static.pepy.tech/badge/maticlib)](https://pepy.tech/project/maticlib)
[![PyPI version](https://badge.fury.io/py/maticlib.svg)](https://badge.fury.io/py/maticlib)

Maticlib is a developer-friendly library designed to build complex, stateful AI workflows with ease. Whether you need a simple chat completion or a multi-node parallel execution graph, Maticlib provides the primitives to build it.

---

## Key Features

### 🤖 Core Agent Framework
Powerful workflow engine with stateful & stateless execution, conditional routing, and multi-state support.

### 🔄 Unified LLM Integration
Deeply integrated support for **OpenAI** (Responses API), **Google Gemini**, and **Mistral AI** with standardized response models.

### 📊 Advanced Response Handling
Track token usage, reasoning tokens (for o-series models), and modality-specific metrics across all providers.

### 🛠️ Developer Experience
Built-in error handling, type-safe design with Pydantic, and comprehensive async support.

### 🎯 Complex Workflows
Conditional branching, parallel node execution, and checkpoint systems to handle real-world automation tasks.

---

## Quick Example

```python
from maticlib.llm.openai import OpenAIClient

# Initialize client (uses OPENAI_API_KEY from environment)
client = OpenAIClient()

# Make a simple request
response = client.complete("Explain quantum computing in one sentence.")
print(client.get_text_response(response))
```

---

## Next Steps

- Check out the [Getting Started](getting_started.md) guide.
- Explore the [API Reference](api/index.md).
- See more [Examples](examples.md).
