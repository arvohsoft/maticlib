<p align="center">
  <img src="https://raw.githubusercontent.com/arvohsoft/maticlib/main/docs/assets/logo.svg" alt="Maticlib Logo" width="220">
</p>

**A high-performance Python Automation Library for Creating Agents.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Downloads](https://static.pepy.tech/badge/maticlib)](https://pepy.tech/project/maticlib)
[![PyPI version](https://badge.fury.io/py/maticlib.svg)](https://badge.fury.io/py/maticlib)

Maticlib is a developer-centric library designed to build complex, stateful AI workflows with ease. Whether you need a simple chat completion or a multi-node parallel execution graph, Maticlib provides the primitives to build it with a focus on type safety and performance.

---

## Documentation

For complete documentation, visit: **[https://arvohsoft.github.io/maticlib/](https://arvohsoft.github.io/maticlib/)**

- [Getting Started](https://arvohsoft.github.io/maticlib/getting_started/)
- [API Reference](https://arvohsoft.github.io/maticlib/api/index.html)
- [Example Gallery](https://arvohsoft.github.io/maticlib/examples/)

---

### Installation

#### From PyPI
```bash
pip install maticlib
```

#### From Source (Local Development)
```bash
# Clone the repository
git clone https://github.com/arvohsoft/maticlib.git
cd maticlib

# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install in editable mode with dev dependencies
pip install -e ".[dev]"
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

## Project Leadership

**Maticlib** is developed and maintained by **Arvoh Software**.

- **Lead Maintainer**: [Anubroto Ghose](https://github.com/anubrotoGhose)
- **Organization**: [Arvoh Software](https://arvohsoft.github.io/arvohsoft/)
- **Contact**: [arvohsoft@gmail.com](mailto:arvohsoft@gmail.com)

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.