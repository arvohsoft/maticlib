# Maticlib

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Downloads](https://static.pepy.tech/badge/maticlib)](https://pepy.tech/project/maticlib)
[![PyPI version](https://badge.fury.io/py/maticlib.svg)](https://badge.fury.io/py/maticlib)
[![Dev Containers: Open](https://img.shields.io/badge/Dev%20Containers-Open-blue)](https://github.com/arvohsoft/maticlib)
[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://github.com/codespaces/new?hide_repo_select=true&ref=main&repo=arvohsoft/maticlib)
[![Open in Codespeed](https://img.shields.io/badge/Codespeed-Open-orange)](https://codespeed.io)
[![Follow @LangChainAI](https://img.shields.io/twitter/follow/LangChainAI?style=social)](https://twitter.com/LangChainAI)

A Python automation library for creating intelligent agents with easy-to-use API client capabilities.

## Features

- 🤖 Simple and intuitive API for building AI agents
- 🔄 Synchronous and asynchronous request support
- 🛠️ Flexible configuration for various inference endpoints
- 📝 Built-in error handling and verbose logging
- 🚀 Lightweight with minimal dependencies

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

```
from maticlib import BaseClientModel

# Initialize the client
client = BaseClientModel(
    inference_url="https://api.example.com/v1/chat/completions",
    header={"Authorization": "Bearer YOUR_API_KEY"},
    model="gpt-3.5-turbo",
    payload={
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": ""}
        ],
        "temperature": 0.7
    },
    verbose=True
)

# Make a synchronous request
response = client.complete("What is the capital of France?")
print(response.json())

# Make an asynchronous request
async_response = await client.async_complete("Tell me a joke")
```

## Usage Examples

### Basic Chat Completion

```
from maticlib import BaseClientModel

client = BaseClientModel(
    inference_url="https://api.openai.com/v1/chat/completions",
    header={"Authorization": "Bearer sk-..."},
    model="gpt-4",
    payload={"messages": [{"role": "user", "content": ""}]}
)

response = client.complete("Hello, how are you?")
```

### Custom Configuration

```
from maticlib import BaseClientModel, ClientError

try:
    client = BaseClientModel(
        inference_url="https://custom-api.com/inference",
        header={
            "Authorization": "Bearer token",
            "Custom-Header": "value"
        },
        model="custom-model-v1",
        payload={
            "messages": [{"role": "user", "content": ""}],
            "max_tokens": 500,
            "temperature": 0.9
        },
        verbose=False
    )
    
    result = client.complete("Your prompt here")
except ClientError as e:
    print(f"Error occurred: {e}")
```

### Asynchronous Usage

```
import asyncio
from maticlib import BaseClientModel

async def main():
    client = BaseClientModel(
        inference_url="https://api.example.com/v1/chat",
        header={"Authorization": "Bearer token"},
        model="model-name"
    )
    
    response = await client.async_complete("Generate a story")
    print(response.json())

asyncio.run(main())
```

## API Reference

### BaseClientModel

The main class for interacting with inference APIs.

#### Parameters

- `inference_url` (str): The endpoint URL for your inference API
- `header` (dict): HTTP headers for authentication and configuration
- `model` (str): The model identifier to use
- `payload` (dict): Base payload structure for requests
- `verbose` (bool): Enable/disable verbose logging (default: True)

#### Methods

##### `complete(prompt: str | list)`

Make a synchronous completion request.

**Parameters:**
- `prompt`: String prompt or list of messages

**Returns:**
- `httpx.Response`: The HTTP response object

##### `async_complete(prompt: str | list)`

Make an asynchronous completion request.

**Parameters:**
- `prompt`: String prompt or list of messages

**Returns:**
- `httpx.Response`: The HTTP response object

## Error Handling

```
from maticlib import BaseClientModel, ClientError

try:
    client = BaseClientModel(...)
    response = client.complete("Your prompt")
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

- [ ] Add streaming response support
- [ ] Implement retry mechanisms
- [ ] Add more authentication methods
- [ ] Comprehensive test coverage
- [ ] Enhanced error handling
- [ ] Documentation improvements

## Acknowledgments

- Built with [httpx](https://www.python-httpx.org/) for modern async HTTP requests
- Inspired by the need for simple, flexible AI agent creation

## Links

- **Homepage**: https://github.com/arvohsoft/maticlib
- **PyPI**: https://pypi.org/project/maticlib/
- **Issues**: https://github.com/arvohsoft/maticlib/issues
- **Changelog**: [CHANGELOG.md](CHANGELOG.md)

---

Made with ❤️ by [Arvoh Software](https://github.com/arvohsoft)
```