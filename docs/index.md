# <img src="https://raw.githubusercontent.com/arvohsoft/maticlib/main/docs/assets/logo.svg" alt="Maticlib Logo" width="180">

**A high-performance Python Automation Library for creating intelligent AI agents.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Downloads](https://static.pepy.tech/badge/maticlib)](https://pepy.tech/project/maticlib)
[![PyPI version](https://badge.fury.io/py/maticlib.svg)](https://badge.fury.io/py/maticlib)

Maticlib is a developer-centric library built to orchestrate complex, stateful AI workflows. Whether you're building simple single-turn bots or massive multi-agent parallel graphs, Maticlib provides the primitives needed to ensure type safety, performance, and cross-provider consistency.

---

## :material-star: Key Features

### :material-robot-outline: Core Agent Framework
The `MaticGraph` workflow engine supports both stateful and stateless execution, conditional routing, and advanced loop prevention.

### :material-sync: Unified LLM Integration
A single, consistent interface for **OpenAI** (Responses API), **Google Gemini**, and **Mistral AI** ensures portability and ease of use.

### :material-chart-timeline-variant: Advanced Telemetry
Track token usage across all modalities, including reasoning tokens for newer models, to optimize cost and performance.

### :material-code-json: Structured Response Parsing
Automatically parse and validate LLM outputs into **Pydantic models**, JSON, or XML. Maticlib handles the prompt engineering and extraction for you.

### :material-layers-outline: Type-Safe Orchestration
Deep integration with Pydantic ensures your workflow states and model responses are always valid and well-defined.

---

## :material-lightning-bolt: Quick Example

```python
from maticlib.llm.openai import OpenAIClient

# Initialize client (uses OPENAI_API_KEY from environment)
client = OpenAIClient()

# Make a simple request
response = client.complete("Describe the benefit of graph-based AI orbits.")
print(client.get_text_response(response))
```

---

## :material-office-building: Maintained By

Maticlib is maintained and developed by **Arvoh Software**.

- **Website**: [arvohsoft.github.io/arvohsoft/](https://arvohsoft.github.io/arvohsoft/)
- **Project Lead**: [Anubroto Ghose](https://github.com/anubrotoGhose)
