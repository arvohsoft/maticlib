<p align="center">
  <img src="https://raw.githubusercontent.com/arvohsoft/maticlib/main/docs/assets/logo.svg" alt="Maticlib Logo" width="220">
  <br>
  <!-- Fallback Logo if Image Fails to Load -->
  <svg width="120" height="32" xmlns="http://www.w3.org/2000/svg" style="display:none;">
    <text x="0" y="24" font-family="Arial, sans-serif" font-size="24" font-weight="bold" fill="#10b981">Maticlib</text>
  </svg>
</p>

**A high-performance Python Automation Library for creating intelligent AI agents.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Downloads](https://static.pepy.tech/badge/maticlib)](https://pepy.tech/project/maticlib)
[![PyPI version](https://badge.fury.io/py/maticlib.svg)](https://badge.fury.io/py/maticlib)

Maticlib is a developer-centric library designed to build complex, stateful AI workflows with ease. Whether you need a simple chat completion or a multi-node parallel execution graph, Maticlib provides the primitives to build it with a focus on type safety and performance.

---

## Key Features

- **Core Agent Framework**: Pure-Python graph workflow engine (`MaticGraph`) supporting both stateful and stateless execution.
- **Unified LLM Integration**: Single interface for **OpenAI** (modern Responses API), **Google Gemini**, and **Mistral AI**.
- **Complex Orchestration**: Built-in support for conditional routing, parallel node execution, and loop prevention.
- **Data Integrity**: Deep Pydantic integration for standardized response models and type-safe workflow states.
- **Advanced Telemetry**: Detailed token usage tracking, including modalities and reasoning tokens for newer models.

---

## Documentation

For complete documentation, visit: **[https://arvohsoft.github.io/maticlib/](https://arvohsoft.github.io/maticlib/)**

- [Getting Started](https://arvohsoft.github.io/maticlib/getting_started/)
- [API Reference](https://arvohsoft.github.io/maticlib/api/index.html)
- [Example Gallery](https://arvohsoft.github.io/maticlib/examples/)

---

## Installation

```bash
pip install maticlib
```

---

## Quick Start

```python
from maticlib.llm.openai import OpenAIClient

# Initialize client (uses OPENAI_API_KEY from environment)
client = OpenAIClient()

# Make a request
response = client.complete("Explain quantum computing in one sentence.")
print(client.get_text_response(response))
```

---

## Roadmap

### Core Library
- [x] Google Gemini integration
- [x] Mistral AI integration
- [x] OpenAI Responses API integration
- [x] Graph-based workflow engine
- [x] Parallel node execution
- [x] Automated documentation system
- [ ] Anthropic Claude integration
- [ ] Streaming support for all providers

### Advanced Features
- [ ] Unified tool/function calling interface
- [ ] Multi-agent collaboration protocols
- [ ] MCP (Model Context Protocol) support
- [ ] Workflow persistence & checkpointing

---

## Project Leadership

**Maticlib** is developed and maintained by **Arvoh Software**.

- **Lead Maintainer**: [Anubroto Ghose](https://github.com/anubrotoGhose)
- **Organization**: [Arvoh Software](https://arvohsoft.github.io/arvohsoft/)
- **Contact**: [arvohsoft@gmail.com](mailto:arvohsoft@gmail.com)

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.