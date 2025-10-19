# Maticlib

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Downloads](https://static.pepy.tech/badge/maticlib)](https://pepy.tech/project/maticlib)
[![PyPI version](https://badge.fury.io/py/maticlib.svg)](https://badge.fury.io/py/maticlib)
[![Dev Containers: Open](https://img.shields.io/badge/Dev%20Containers-Open-blue)](https://github.com/arvohsoft/maticlib)
[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://github.com/codespaces/new?hide_repo_select=true&ref=main&repo=arvohsoft/maticlib)

A Python automation library for creating intelligent agents with easy-to-use API clients for multiple LLM providers including Google Gemini and Mistral AI.

## Features

- 🤖 Simple and intuitive API for building AI agents
- 🔄 Synchronous and asynchronous request support
- 🛠️ Multiple LLM provider support (Google Gemini, Mistral AI)
- 📝 Built-in error handling and verbose logging
- 🚀 Lightweight with minimal dependencies
- 🔑 Environment variable support for API keys
- 💬 Multi-turn conversation support

## Installation

### From PyPI (Production)

```
pip install maticlib
```

### From TestPyPI (Development)

```
pip install -i https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ maticlib
```

### From Source

```
git clone https://github.com/arvohsoft/maticlib.git
cd maticlib
pip install -e .
```

## Quick Start

### Google Gemini

```
from maticlib.llm.google_genai import GoogleGenAIClient

# Initialize with API key
client = GoogleGenAIClient(api_key="YOUR_GOOGLE_API_KEY")

# Or use environment variable GOOGLE_API_KEY
client = GoogleGenAIClient()

# Make a request
response = client.complete("Hello! Tell me about Python")
print(response.json())
```

### Mistral AI

```
from maticlib.llm.mistral import MistralClient

# Initialize with API key
client = MistralClient(api_key="YOUR_MISTRAL_API_KEY")

# Or use environment variable MISTRAL_API_KEY
client = MistralClient()

# Make a request
response = client.complete("What is the best French cheese?")
print(response.json())
```

### Generic Client

```
from maticlib.core.client import BaseClientModelURL

# For custom API endpoints
client = BaseClientModelURL(
    inference_url="https://api.example.com/v1/chat",
    header={"Authorization": "Bearer YOUR_API_KEY"},
    model="model-name",
    payload={"messages": []},
    verbose=True
)

response = client.complete("Your prompt here")
```

## Usage Examples

### Google Gemini with Custom Configuration

```
from maticlib.llm.google_genai import GoogleGenAIClient

client = GoogleGenAIClient(
    model="gemini-2.5-flash",  # or "gemini-pro", etc.
    api_key="YOUR_API_KEY",
    thinking_budget=0,
    verbose=True
)

response = client.complete("Explain quantum computing")
print(response.json())
```

### Mistral AI with Different Models

```
from maticlib.llm.mistral import MistralClient

# Use different Mistral models
client = MistralClient(
    model="mistral-large-latest",  # or "mistral-medium-latest", "mistral-small-latest"
    api_key="YOUR_API_KEY"
)

response = client.complete("Write a short poem about coding")
print(response.json())
```

### Multi-turn Conversations

```
from maticlib.llm.mistral import MistralClient

client = MistralClient(api_key="YOUR_API_KEY")

# Pass conversation history as list of messages
messages = [
    {"role": "user", "content": "Hello!"},
    {"role": "assistant", "content": "Hi! How can I help you?"},
    {"role": "user", "content": "What's the weather like?"}
]

response = client.complete(messages)
print(response.json())
```

### Asynchronous Usage

```
import asyncio
from maticlib.llm.google_genai import GoogleGenAIClient

async def main():
    client = GoogleGenAIClient(api_key="YOUR_API_KEY")
    response = await client.async_complete("Tell me a joke")
    print(response.json())

asyncio.run(main())
```

## API Reference

### GoogleGenAIClient

Client for Google Gemini API.

#### Parameters

- `model` (str): Model name (default: "gemini-2.5-flash")
- `api_key` (str): Google API key (or use GOOGLE_API_KEY env var)
- `thinking_budget` (int): Budget for model thinking (default: 0)
- `verbose` (bool): Enable verbose logging (default: True)

#### Methods

##### `complete(prompt: str) -> httpx.Response`

Make a synchronous completion request.

##### `async_complete(prompt: str) -> httpx.Response`

Make an asynchronous completion request.

### MistralClient

Client for Mistral AI API.

#### Parameters

- `model` (str): Model name (default: "mistral-large-latest")
- `api_key` (str): Mistral API key (or use MISTRAL_API_KEY env var)
- `verbose` (bool): Enable verbose logging (default: True)

#### Methods

##### `complete(prompt: str | list) -> httpx.Response`

Make a synchronous completion request. Accepts string or message list.

##### `async_complete(prompt: str | list) -> httpx.Response`

Make an asynchronous completion request. Accepts string or message list.

### BaseClientModelURL

Generic client for custom API endpoints.

#### Parameters

- `inference_url` (str): API endpoint URL
- `header` (dict): HTTP headers for authentication
- `model` (str): Model identifier
- `payload` (dict): Base payload structure
- `verbose` (bool): Enable verbose logging (default: True)

## Environment Variables

Set environment variables for automatic API key loading:

```
export GOOGLE_API_KEY="your-google-api-key"
export MISTRAL_API_KEY="your-mistral-api-key"
```

Then use clients without explicitly passing keys:

```
from maticlib.llm.google_genai import GoogleGenAIClient
from maticlib.llm.mistral import MistralClient

google_client = GoogleGenAIClient()  # Uses GOOGLE_API_KEY
mistral_client = MistralClient()      # Uses MISTRAL_API_KEY
```

## Error Handling

```
from maticlib.llm.mistral import MistralClient
from maticlib.exceptions import ClientError

try:
    client = MistralClient(api_key="YOUR_API_KEY")
    response = client.complete("Your prompt")
    print(response.json())
except ClientError as e:
    print(f"Client error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Development

### Setting Up Development Environment

```
# Clone the repository
git clone https://github.com/arvohsoft/maticlib.git
cd maticlib

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -e ".[dev]"
```

### Running Tests

```
pytest
```

### Code Formatting

```
black maticlib/
```

### Type Checking

```
mypy maticlib/
```

## Requirements

- Python >= 3.8
- httpx >= 0.24.0

## Supported LLM Providers

- **Google Gemini** - All Gemini models (gemini-2.5-flash, gemini-pro, etc.)
- **Mistral AI** - All Mistral models (mistral-large-latest, mistral-medium-latest, etc.)
- **Custom** - Any OpenAI-compatible API endpoint

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For support, email arvohsoft@gmail.com or open an issue on GitHub.

## Roadmap

### LLM Provider Support
- [x] Google Gemini integration
- [x] Mistral AI integration
- [ ] OpenAI integration
- [ ] Anthropic Claude integration
- [ ] Cohere integration
- [ ] AWS Bedrock integration
- [ ] Ollama integration (local models)

### Tool Integration & Function Calling
- [ ] Unified tool/function calling interface across all LLM providers
- [ ] Tool schema validation and type checking
- [ ] Built-in tool registry for common operations (web search, file operations, calculations)
- [ ] Custom tool creation framework with decorators
- [ ] Automatic tool result formatting and error handling
- [ ] Tool execution tracking and logging

### Output Standardization
- [ ] Unified response format across all LLM providers
- [ ] Pydantic-based structured output support
- [ ] JSON schema validation for all responses
- [ ] Automatic type conversion and serialization
- [ ] Response normalization layer
- [ ] Provider-agnostic result objects

### Orchestration & Workflow
- [ ] Graph-based workflow engine for complex agent interactions
- [ ] Visual workflow builder and debugger
- [ ] Conditional branching and parallel execution
- [ ] State management across workflow steps
- [ ] Loop detection and prevention
- [ ] Workflow templates for common patterns
- [ ] Event-driven execution model

### Agent Framework
- [ ] Standalone agent creation with custom roles and goals
- [ ] Multi-agent collaboration system
- [ ] Agent communication protocols
- [ ] Task delegation and assignment
- [ ] Shared memory and knowledge base between agents
- [ ] Agent hierarchies and teams
- [ ] Dynamic agent creation and termination
- [ ] Agent performance monitoring

### Model Context Protocol (MCP)
- [ ] MCP client implementation for consuming external tools
- [ ] MCP server implementation for exposing tools
- [ ] Resource and prompt management via MCP
- [ ] Support for MCP transport layers (stdio, HTTP)
- [ ] Built-in MCP tool registry
- [ ] MCP session management

### Prompt Management
- [ ] Centralized prompt hub with curated templates
- [ ] Prompt versioning and A/B testing
- [ ] Prompt optimization suggestions
- [ ] Domain-specific prompt collections (coding, writing, analysis)
- [ ] Prompt chaining and composition
- [ ] Variable interpolation and templating
- [ ] Multilingual prompt support

### Terminal User Interface (TUI)
- [ ] Rich terminal output with color-coded messages
- [ ] Real-time tool execution visualization
- [ ] Progress bars for long-running operations
- [ ] Interactive agent conversation display
- [ ] Workflow step visualization
- [ ] Error highlighting and debugging info
- [ ] Configurable verbosity levels
- [ ] Export TUI sessions to logs

### Telemetry & Observability
- [ ] OpenTelemetry integration
- [ ] Request/response tracing
- [ ] Cost tracking per provider
- [ ] Token usage analytics
- [ ] Performance metrics (latency, throughput)
- [ ] Error rate monitoring
- [ ] Custom metric collection
- [ ] Integration with observability platforms (Prometheus, Grafana)

### Core Improvements
- [ ] Streaming response support for all providers
- [ ] Automatic retry mechanisms with exponential backoff
- [ ] Circuit breaker pattern for provider failures
- [ ] Request rate limiting and queuing
- [ ] Response caching layer
- [ ] Comprehensive test coverage (>90%)
- [ ] Enhanced error handling with detailed error types
- [ ] Async-first architecture throughout

### Developer Experience
- [ ] Interactive CLI for quick testing
- [ ] VSCode extension for code completion
- [ ] Comprehensive API documentation with examples
- [ ] Tutorial notebooks and video guides
- [ ] Migration guides from other frameworks
- [ ] Community-contributed recipes
- [ ] Performance benchmarking tools

### Security & Compliance
- [ ] API key rotation and management
- [ ] Request encryption and signing
- [ ] PII detection and filtering
- [ ] Audit logging
- [ ] Role-based access control
- [ ] Compliance reporting (GDPR, SOC2)

### Advanced Features
- [ ] Fine-tuning management interface
- [ ] Model evaluation and benchmarking suite
- [ ] Prompt injection detection
- [ ] Content moderation and safety filters
- [ ] Multi-modal support (images, audio, video)
- [ ] Vector database integration
- [ ] RAG (Retrieval-Augmented Generation) framework
- [ ] Agent memory persistence (short-term, long-term)

## Acknowledgments

- Built with [httpx](https://www.python-httpx.org/) for modern async HTTP requests
- Inspired by the need for simple, flexible AI agent creation
- Supports Google Gemini and Mistral AI APIs

## Links

- **Homepage**: https://github.com/arvohsoft/maticlib
- **PyPI**: https://pypi.org/project/maticlib/
- **Issues**: https://github.com/arvohsoft/maticlib/issues
- **Changelog**: [CHANGELOG.md](CHANGELOG.md)

---

## About

Maticlib is developed and maintained by **Arvoh Software**.

**Main Contributor:** [Anubroto Ghose](https://github.com/anubrotoGhose)<br>
**Organization:** [Arvoh Software](https://github.com/arvohsoft)  
**Email:** arvohsoft@gmail.com

Made with ❤️ for developers building intelligent AI agents

### Contributors

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for details on how to get involved.