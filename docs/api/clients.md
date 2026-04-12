# LLM Clients

Maticlib provides a unified interface for multiple LLM providers. All clients inherit from `BaseLLMClient` and support both synchronous and asynchronous completion.

## OpenAI Client

Using the modern OpenAI Responses API.

::: maticlib.llm.openai.client.OpenAIClient

## Mistral Client

::: maticlib.llm.mistral.client.MistralClient

## Google GenAI Client

::: maticlib.llm.google_genai.client.GoogleGenAIClient

## Response Models

Standardized models used to ensure consistency across providers.

### OpenAI Response
::: maticlib.llm.openai.openai_classes.OpenAIResponse

### Mistral Response
::: maticlib.llm.mistral.mistral_classes.MistralResponse

### Gemini Response
::: maticlib.llm.google_genai.gemini_classes.GeminiResponse
