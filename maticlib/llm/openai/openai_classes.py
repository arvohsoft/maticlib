"""
OpenAI Response Pydantic Models
================================
Structured models for the OpenAI Responses API (/v1/responses endpoint).

The Responses API returns richer structured output than the older Chat
Completions endpoint. Key differences surfaced here:
  - Output is a *list* of typed items (message, reasoning, tool_use, etc.)
  - Usage includes `input_tokens_details` (cache hits) and
    `output_tokens_details` (reasoning tokens for o-series models)
  - There is a top-level `status` field per response AND per output item

All common fields (content, content_parts, tokens, response_id, raw_response)
are mapped onto the shared `LLMResponseBase` so callers can treat every
provider uniformly.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, computed_field, ConfigDict

from maticlib.client.classes.client_output_model import LLMResponseBase
from maticlib.client.classes.enums.modality_type import ModalityType
from maticlib.client.classes.model_classes.content_part import ContentPart


# ---------------------------------------------------------------------------
# Token-usage sub-models
# ---------------------------------------------------------------------------

class OpenAIOutputTokenDetails(BaseModel):
    """
    Granular breakdown of *output* (completion-side) token usage.

    Attributes:
        reasoning_tokens (int): Tokens consumed by internal chain-of-thought
            reasoning. Non-zero only on o-series models (o1, o3, o4, ...).
    """
    reasoning_tokens: int = Field(0, description="Tokens used for internal model reasoning")

    model_config = ConfigDict(extra="allow")


class OpenAIInputTokenDetails(BaseModel):
    """
    Granular breakdown of *input* (prompt-side) token usage.

    Attributes:
        cached_tokens (int): Tokens served from the prompt cache, meaning
            they were already in the KV-cache and cost less.
        audio_tokens (int): Tokens attributed to audio input content.
    """
    cached_tokens: int = Field(0, description="Tokens served from the prompt cache")
    audio_tokens: int = Field(0, description="Tokens attributed to audio input")

    model_config = ConfigDict(extra="allow")


class OpenAIUsage(BaseModel):
    """
    Full token-usage block returned by the OpenAI Responses API.

    Attributes:
        input_tokens (int): Total tokens in the prompt / input messages.
        output_tokens (int): Total tokens in the completion / output items.
        total_tokens (int): Sum of input and output tokens.
        output_tokens_details (OpenAIOutputTokenDetails): Per-type output breakdown.
        input_tokens_details (OpenAIInputTokenDetails): Per-type input breakdown.
    """
    input_tokens: int = Field(..., description="Total input (prompt) tokens")
    output_tokens: int = Field(..., description="Total output (completion) tokens")
    total_tokens: int = Field(..., description="Total tokens used")
    output_tokens_details: Optional[OpenAIOutputTokenDetails] = Field(
        None, description="Granular output-token breakdown"
    )
    input_tokens_details: Optional[OpenAIInputTokenDetails] = Field(
        None, description="Granular input-token breakdown"
    )

    model_config = ConfigDict(extra="allow")


# ---------------------------------------------------------------------------
# Output item sub-models
# ---------------------------------------------------------------------------

class OpenAIOutputContentItem(BaseModel):
    """
    A single piece of content inside an output message.

    Attributes:
        type (str): Content type, e.g. ``output_text`` or ``refusal``.
        text (str, optional): The actual text when type is ``output_text``.
        annotations (list): Any inline annotations on the text.
    """
    type: str = Field(..., description="Content part type (output_text, refusal, ...)")
    text: Optional[str] = Field(None, description="Text payload for output_text parts")
    annotations: Optional[List[Any]] = Field(
        default_factory=list, description="Inline annotations on the text content"
    )

    model_config = ConfigDict(extra="allow")


class OpenAIOutputMessage(BaseModel):
    """
    A single *output item* as returned by the Responses API.

    Attributes:
        id (str): Unique ID of this output item (e.g. ``msg_...``).
        type (str): Item type: ``message``, ``reasoning``, ``tool_use``, etc.
        status (str): Item-level status (``completed``, ``failed``, ...).
        role (str): Speaker role for message items, typically ``assistant``.
        content (List[OpenAIOutputContentItem]): Structured content parts.
    """
    id: str = Field(..., description="Unique output-item ID")
    type: str = Field(..., description="Output item type (message, reasoning, tool_use, ...)")
    status: Optional[str] = Field(None, description="Per-item completion status")
    role: Optional[str] = Field(None, description="Speaker role (assistant, tool, ...)")
    content: Optional[List[OpenAIOutputContentItem]] = Field(
        default_factory=list, description="Structured content parts for this item"
    )

    model_config = ConfigDict(extra="allow")


# ---------------------------------------------------------------------------
# Top-level response model
# ---------------------------------------------------------------------------

class OpenAIResponse(LLMResponseBase):
    """
    OpenAI Responses API response (/v1/responses).

    Maps the raw JSON payload onto the shared ``LLMResponseBase`` interface
    so callers can use ``response.content`` and ``response.content_parts``
    the same way they would with ``MistralResponse`` or ``GeminiResponse``.

    Common (inherited) fields populated automatically:
        content          -- concatenated text from all output_text parts
        content_parts    -- one ContentPart per output_text chunk
        prompt_tokens    -- mapped from usage.input_tokens
        completion_tokens-- mapped from usage.output_tokens
        total_tokens     -- mapped from usage.total_tokens
        finish_reason    -- mapped from first output item's status
        response_id      -- mapped from top-level id
        raw_response     -- original JSON dict

    OpenAI-specific fields:
        id (str): Response ID (resp_...).
        object (str): Always "response".
        created_at (int): Unix timestamp of creation.
        status (str): Response-level status (completed, failed, ...).
        output (List[OpenAIOutputMessage]): Ordered list of output items.
        usage (OpenAIUsage): Detailed token-usage breakdown.
        model_version (str): Model string echoed back by OpenAI.
    """

    # ---- OpenAI-specific top-level fields ----
    id: str = Field(..., description="Response ID (resp_...)")
    object: str = Field(..., description="Object type, always 'response'")
    created_at: int = Field(..., description="Unix timestamp of creation")
    status: str = Field(..., description="Top-level response status")
    output: List[OpenAIOutputMessage] = Field(
        default_factory=list, description="Ordered output items"
    )
    usage: Optional[OpenAIUsage] = Field(None, description="Detailed token usage")
    model_version: Optional[str] = Field(
        None, description="Model string as returned by OpenAI"
    )

    def __init__(self, **data: Any) -> None:
        # ------------------------------------------------------------------
        # 1. Walk every output item and extract text into content / content_parts
        # ------------------------------------------------------------------
        text_parts: List[str] = []
        content_parts: List[ContentPart] = []

        for item in data.get("output", []):
            if not isinstance(item, dict):
                continue
            for part in item.get("content", []):
                if not isinstance(part, dict):
                    continue
                if part.get("type") == "output_text" and part.get("text"):
                    text_parts.append(part["text"])
                    content_parts.append(
                        ContentPart(type=ModalityType.TEXT, text=part["text"])
                    )

        if text_parts:
            data["content"] = " ".join(text_parts)
        if content_parts:
            data["content_parts"] = content_parts

        # ------------------------------------------------------------------
        # 2. Map usage onto the shared LLMResponseBase token fields
        # ------------------------------------------------------------------
        usage_raw = data.get("usage") or {}
        if isinstance(usage_raw, dict):
            data["prompt_tokens"] = usage_raw.get("input_tokens")
            data["completion_tokens"] = usage_raw.get("output_tokens")
            data["total_tokens"] = usage_raw.get("total_tokens")

        # ------------------------------------------------------------------
        # 3. finish_reason -- use the status of the first output item
        # ------------------------------------------------------------------
        output_list = data.get("output") or []
        if output_list and isinstance(output_list[0], dict):
            data["finish_reason"] = output_list[0].get("status")

        # ------------------------------------------------------------------
        # 4. Align shared identifier / metadata fields
        # ------------------------------------------------------------------
        data["response_id"] = data.get("id")
        # 'model' is the field in LLMResponseBase; copy to model_version too
        data["model_version"] = data.get("model")

        # Preserve raw JSON before super().__init__ may alter data
        data["raw_response"] = data.copy()

        super().__init__(**data)

    # ------------------------------------------------------------------
    # Convenience properties for OpenAI-specific metadata
    # ------------------------------------------------------------------

    @computed_field
    @property
    def timestamp(self) -> datetime:
        """Converts the ``created_at`` Unix timestamp into a ``datetime`` object."""
        return datetime.fromtimestamp(self.created_at)

    @property
    def reasoning_tokens(self) -> Optional[int]:
        """
        Tokens used for internal model reasoning (o-series models only).

        Returns ``None`` for standard GPT models that do not expose
        reasoning-token counts.
        """
        if self.usage and self.usage.output_tokens_details:
            return self.usage.output_tokens_details.reasoning_tokens
        return None

    @property
    def cached_tokens(self) -> Optional[int]:
        """
        Input tokens served from the prompt cache.

        A non-zero value means the model reused previously computed KV-cache
        entries, which are billed at a reduced rate.
        """
        if self.usage and self.usage.input_tokens_details:
            return self.usage.input_tokens_details.cached_tokens
        return None
