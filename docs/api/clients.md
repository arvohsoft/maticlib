# :material-robot-outline: LLM Clients API Reference

Maticlib provides a unified interface for multiple LLM providers. All clients inherit from `BaseLLMClient` and support both synchronous and asynchronous completion.

## OpenAI Client

Using the modern OpenAI Responses API.

::: maticlib.llm.openai.client.OpenAIClient

## Mistral Client

Using the native Mistral AI Chat Completions API.

::: maticlib.llm.mistral.client.MistralClient

## Google GenAI Client

Using the Google Gemini Developer API.

::: maticlib.llm.google_genai.client.GoogleGenAIClient

---

## :material-card-account-details-outline: Response Models

Standardized models used to ensure consistency across providers. 

### **OpenAI Response (`OpenAIResponse`)**

All OpenAI clients return an `OpenAIResponse` containing both general and provider-specific fields.

#### **Common (Inherited) Fields**

| Field | Type | Source Mapping |
| :--- | :--- | :--- |
| `content` | `str` | Concatenated text from all `output_text` parts. |
| `content_parts` | `List[ContentPart]` | Exactly one `ContentPart` per `output_text` chunk. |
| `prompt_tokens` | `int` | Mapped from `usage.input_tokens`. |
| `completion_tokens` | `int` | Mapped from `usage.output_tokens`. |
| `total_tokens` | `int` | Mapped from `usage.total_tokens`. |
| `finish_reason` | `str` | Mapped from the first output item's status. |
| `response_id` | `str` | Mapped from top-level `id`. |
| `raw_response` | `Dict[str, Any]` | The original, full JSON response dictionary. |

#### **OpenAI-Specific Fields**

| Field | Type | Description |
| :--- | :--- | :--- |
| `id` | `str` | Response ID (prefixed with `resp_`). |
| `object` | `str` | Always `"response"`. |
| `created_at` | `int` | Unix timestamp of creation. |
| `status` | `str` | Response-level status (e.g. `completed`, `failed`). |
| `output` | `List[OpenAIOutputMessage]` | Ordered list of output items returned by the API. |
| `usage` | `OpenAIUsage` | Detailed token-usage breakdown. |
| `model_version` | `str` | Model version string echoed back by OpenAI. |

#### **OpenAI-Specific Properties**

| Property | Type | Description |
| :--- | :--- | :--- |
| `cached_tokens` | `int` | Input tokens served from the prompt cache. A non-zero value means the model reused previously computed KV-cache entries. |
| `reasoning_tokens` | `int \| None` | Tokens used for internal model reasoning (o-series models only). Returns `None` for standard models. |
| `timestamp` | `datetime` | Converts the `created_at` Unix timestamp into a `datetime` object. |

::: maticlib.llm.openai.openai_classes.OpenAIResponse

### **Mistral Response (`MistralResponse`)**

`maticlib.llm.mistral.mistral_classes.MistralResponse`

Bases: `LLMResponseBase`

Mistral-specific response structure. Supports both text-only and multimodal (Pixtral) models. Inherits from `LLMResponseBase` and adds Mistral-specific fields.

#### **Mistral-Specific Properties**

##### **`timestamp`**

*Convert Unix timestamp to datetime.*

::: maticlib.llm.mistral.mistral_classes.MistralResponse

### **Gemini Response (`GeminiResponse`)**

`maticlib.llm.google_genai.gemini_classes.GeminiResponse`

Bases: `LLMResponseBase`

Gemini-specific response structure. Supports multimodal inputs (text, image, audio, video) and outputs. Inherits from `LLMResponseBase` and adds Gemini-specific fields.

#### **Gemini-Specific Properties**

##### **`cached_token_count`**

*Get cached content token count (Gemini context caching).*

##### **`thoughts_token_count`**

*Get the thoughts token count if available (Gemini-specific).*

::: maticlib.llm.google_genai.gemini_classes.GeminiResponse

