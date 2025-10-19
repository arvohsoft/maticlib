# Contributing to Maticlib

First off, thank you for considering contributing to Maticlib! ❤️

All types of contributions are encouraged and valued. Whether you're fixing bugs, adding new features, improving documentation, or spreading the word about Maticlib, your help is appreciated.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [How Can I Contribute?](#how-can-i-contribute)
  - [Reporting Bugs](#reporting-bugs)
  - [Suggesting Features](#suggesting-features)
  - [Adding LLM Provider Support](#adding-llm-provider-support)
  - [Improving Documentation](#improving-documentation)
  - [Code Contributions](#code-contributions)
- [Development Setup](#development-setup)
- [Pull Request Process](#pull-request-process)
- [Style Guidelines](#style-guidelines)
- [Community](#community)

## Code of Conduct

This project and everyone participating in it is governed by our commitment to maintain a welcoming, inclusive, and harassment-free environment. Be respectful, professional, and considerate in all interactions.

## Getting Started

Before you begin:
- Make sure you have Python 3.8 or higher installed
- Familiarize yourself with the project by reading the [README.md](README.md)
- Check existing [issues](https://github.com/arvohsoft/maticlib/issues) and [pull requests](https://github.com/arvohsoft/maticlib/pulls)

## How Can I Contribute?

### Reporting Bugs

Found a bug? Help us fix it!

**Before submitting a bug report:**
- Check if the bug has already been reported in [Issues](https://github.com/arvohsoft/maticlib/issues)
- Use the latest version of Maticlib
- Collect information about the bug (Python version, OS, error messages, minimal code to reproduce)

**How to submit a bug report:**
1. Open a [new issue](https://github.com/arvohsoft/maticlib/issues/new)
2. Use a clear, descriptive title
3. Describe the expected behavior vs actual behavior
4. Provide a minimal code example that reproduces the issue
5. Include your environment details (Python version, OS, Maticlib version)
6. Add any relevant error messages or stack traces

### Suggesting Features

Have an idea to make Maticlib better?

**Before suggesting a feature:**
- Check if it's already been suggested in [Issues](https://github.com/arvohsoft/maticlib/issues)
- Consider if it fits the project's scope (AI agent automation and LLM integration)

**How to suggest a feature:**
1. Open a [new issue](https://github.com/arvohsoft/maticlib/issues/new)
2. Use a clear, descriptive title starting with "Feature:"
3. Explain the problem this feature would solve
4. Describe your proposed solution
5. Provide examples of how it would be used
6. Explain why this would be useful to most users

### Adding LLM Provider Support

Want to add support for a new LLM provider? Great!

**Requirements for new LLM clients:**
- Must support both synchronous and asynchronous requests
- Should follow the existing client patterns (see `GoogleGenAIClient` or `MistralClient`)
- Must include proper error handling
- Should support environment variable configuration for API keys
- Must include usage examples in documentation

**Structure:**
```
maticlib/llm/
└── your_provider_llm/
    ├── __init__.py
    └── client.py
```

### Improving Documentation

Documentation improvements are always welcome:
- Fix typos or clarify confusing sections
- Add more usage examples
- Improve API documentation
- Translate documentation (contact us first)

### Code Contributions

Ready to code? Here's how:

1. **Fork the repository**
2. **Clone your fork:**
   ```
   git clone https://github.com/your-username/maticlib.git
   cd maticlib
   ```

3. **Create a branch:**
   ```
   git checkout -b feature/your-feature-name
   ```

4. **Make your changes** (see [Development Setup](#development-setup))

5. **Test your changes:**
   ```
   pytest
   ```

6. **Commit your changes:**
   ```
   git commit -m "Add: Brief description of changes"
   ```

7. **Push to your fork:**
   ```
   git push origin feature/your-feature-name
   ```

8. **Submit a Pull Request**

## Development Setup

### 1. Set up your environment

```
# Clone the repository
git clone https://github.com/arvohsoft/maticlib.git
cd maticlib

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Install in development mode
pip install -e ".[dev]"
```

### 2. Run tests

```
# Run all tests
pytest

# Run with coverage
pytest --cov=maticlib

# Run specific test file
pytest tests/test_google_genai.py
```

### 3. Format code

```
# Format with black
black maticlib/

# Check formatting
black --check maticlib/
```

### 4. Type checking

```
# Run mypy
mypy maticlib/
```

## Pull Request Process

1. **Update documentation** - If you add features, update the README.md and docstrings
2. **Update CHANGELOG.md** - Add your changes under the `[Unreleased]` section
3. **Follow style guidelines** - Use black for formatting, follow PEP 8
4. **Write tests** - Add tests for new functionality
5. **Update version** - Only if you're a maintainer
6. **Describe your changes** - Write a clear PR description explaining what and why

**PR Title Format:**
- `Add: Description` - New features
- `Fix: Description` - Bug fixes
- `Docs: Description` - Documentation changes
- `Refactor: Description` - Code improvements
- `Test: Description` - Test additions/changes

## Style Guidelines

### Python Code Style

- Follow [PEP 8](https://peps.python.org/pep-0008/)
- Use [Black](https://black.readthedocs.io/) for formatting (line length: 88)
- Use type hints for function signatures
- Write descriptive docstrings (Google style)
- Keep functions focused and small

### Commit Messages

- Use present tense ("Add feature" not "Added feature")
- Use imperative mood ("Move cursor to..." not "Moves cursor to...")
- Keep first line under 50 characters
- Reference issues and PRs when relevant

Example:
```
Add MistralClient for Mistral AI integration

- Implement sync and async completion methods
- Add environment variable support for API key
- Include usage examples in documentation

Closes #42
```

### Documentation Style

- Use clear, simple language
- Include code examples for features
- Keep README.md up to date
- Add inline comments for complex logic only

## Community

### Getting Help

- **Questions?** Open an [issue](https://github.com/arvohsoft/maticlib/issues) with the "question" label
- **Email:** arvohsoft@gmail.com
- **Discussions:** Use GitHub Discussions (if enabled)

### Recognition

Contributors are recognized in:
- The project's README.md
- Release notes in CHANGELOG.md
- GitHub's contributor statistics

## Development Roadmap

Check our [Roadmap](README.md#roadmap) to see what we're working on. Great first contributions:
- Adding new LLM provider support (OpenAI, Anthropic, Cohere)
- Improving error messages
- Adding more usage examples
- Writing tests

## Questions?

Don't hesitate to ask! Open an issue, send an email, or start a discussion. We're here to help you contribute successfully.

---

**Thank you for contributing to Maticlib!**

*Maintained by [Arvoh Software](https://github.com/arvohsoft) | Lead Developer: Anubroto Ghose*