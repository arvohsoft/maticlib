# Getting Started

Follow this guide to get up and running with Maticlib.

## Installation

Install Maticlib using pip:

```bash
pip install maticlib
```

### From Source

If you want the latest features or wish to contribute:

```bash
git clone https://github.com/arvohsoft/maticlib.git
cd maticlib
pip install -e .
```

---

## Environment Configuration

Maticlib supports environment variables for secure API key management. We recommend using a `.env` file in your project root.

```bash
# .env
OPENAI_API_KEY=your_openai_key
MISTRAL_API_KEY=your_mistral_key
GOOGLE_API_KEY=your_google_key
```

Then in your code:

```python
from dotenv import load_dotenv
load_dotenv()
```

---

## Core Concepts

### LLM Clients
Maticlib provides a unified interface for multiple LLM providers. Each client supports synchronous (`complete`) and asynchronous (`async_complete`) methods.

```python
from maticlib.llm.mistral import MistralClient

client = MistralClient()
response = client.complete("Hello!")
```

### Graph Workflows
The `MaticGraph` is a powerful engine for building agentic workflows as a directed graph of nodes.

```python
from maticlib.graph import MaticGraph

graph = MaticGraph()
graph.add_node("start", lambda state: {"status": "running"}, next="end")
graph.add_node("end", lambda state: {"status": "complete"})

result = graph.run(initial_state={})
```

---

## Next Steps

Now that you have the basics down, explore the [API Reference](api/index.md) or look at some [Examples](examples.md).
