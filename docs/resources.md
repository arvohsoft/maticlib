# Resources & Development

Find everything you need to dive deeper into Maticlib, from architectural resources to contribution guidelines and performance standards.

---

## :material-book-open-outline: Core Resources

Access key information about the library's design and usage patterns:

- **[Modules Overview](https://arvohsoft.github.io/maticlib/modules/)**: A structured, deep-dive into each individual Maticlib component.
- **[API Reference](https://arvohsoft.github.io/maticlib/api/)**: Fully documented technical specifications, parameters, and return types.
- **[Example Suite](https://arvohsoft.github.io/maticlib/examples/)**: A rich gallery of interactive scripts and real-world usage patterns.
- **[SQL & Data Validation](https://arvohsoft.github.io/maticlib/modules/text2sql/)**: Details on transpilation, SQL injection guards with `sqlglot`, and secure execution.
- **[RAG Evaluation](https://arvohsoft.github.io/maticlib/modules/evaluation/)**: Reference guide for testing token overlap relevance and using LLM-as-a-judge evaluators.
- **[Pydantic Documentation](https://docs.pydantic.dev/)**: Essential reading for understanding our schema validation and state management.

---

## :material-hand-pointing-right: How to Contribute

We welcome contributions of all types! Whether you are a developer looking to add a new provider or a user reporting a bug, your input is valuable.

1.  **Pick an Issue**: Check out our [GitHub Issues](https://github.com/arvohsoft/maticlib/issues) for tasks that need attention.
2.  **Submit a Pull Request**: Follow our standard process—fork the repo, create a feature branch, and submit your PR.
3.  **Improve Documentation**: If you find a typo or an unclear example, pull requests for documentation are always appreciated.

---

## :material-rocket-launch-outline: Performance Standards

When contributing code, please ensure it meets the following performance goals:

- **Minimal Latency**: Avoid any blocking calls within the graph engine to ensure smooth workflow execution.
- **Memory Efficiency**: Be mindful of state object sizes, especially in long-running or large-scale workflows.
- **Async-First**: Prioritize providing asynchronous alternatives (`async_`) for any new I/O operations.

---

## :material-account-group-outline: Community Involvement

You can contribute to the project's growth without writing a single line of code:

- **Report Bugs**: Help us find and fix issues by opening [detailed issues](https://github.com/arvohsoft/maticlib/issues).
- **Propose Features**: Suggest new LLM providers or graph primitives.
- **Share Use Cases**: We love hearing about the unique graph workflows you build.

---

## :material-message-outline: Support & Feedback

If you have questions or need support:
- Open an issue on GitHub.
- Email the maintainers at [arvohsoft@gmail.com](mailto:arvohsoft@gmail.com).
