"""
LLM Response Pydantic Models - Multimodal Ready
================================================
Base class and derived classes for LLM Responses
Supports text-only and multimodal (image, audio, video) inputs/outputs.
"""

from typing import Optional, List, Dict, Any, Union, Literal
from pydantic import BaseModel, Field, computed_field
from enum import Enum

# ============================================================================
# ENUMS AND TYPE DEFINITIONS
# ============================================================================

class ModalityType(str, Enum):
    """Supported modality types"""
    TEXT = "text"
    IMAGE = "image"
    AUDIO = "audio"
    VIDEO = "video"
    UNKNOWN = "unknown"


class RoleType(str, Enum):
    """Role types in conversation"""
    USER = "user"
    ASSISTANT = "assistant"
    MODEL = "model"
    SYSTEM = "system"


# ============================================================================
# COMMON CONTENT CLASSES
# ============================================================================

class ContentPart(BaseModel):
    """Generic content part that can represent any modality"""
    type: ModalityType = Field(default=ModalityType.TEXT, description="Type of content")
    text: Optional[str] = Field(None, description="Text content")
    image_url: Optional[str] = Field(None, description="Image URL or data URI")
    video_url: Optional[str] = Field(None, description="Video URL or data URI")
    audio_url: Optional[str] = Field(None, description="Audio URL or data URI")
    inline_data: Optional[Dict[str, Any]] = Field(None, description="Inline binary data with mime type")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")
    
    class Config:
        extra = "allow"


# ============================================================================
# BASE CLASS - Common fields across both APIs
# ============================================================================

class LLMResponseBase(BaseModel):
    """
    Base class for LLM API responses with common fields.
    
    This class provides a unified interface for both Mistral and Gemini responses,
    supporting both text-only and multimodal inputs/outputs.
    """
    
    model: str = Field(..., description="Model identifier/version used for generation")
    content: Optional[str] = Field(None, description="Primary text content (extracted from parts)")
    content_parts: Optional[List[ContentPart]] = Field(None, description="Structured multimodal content parts")
    finish_reason: Optional[str] = Field(None, description="Reason for completion")
    
    # Token usage information (common across both)
    prompt_tokens: Optional[int] = Field(None, description="Number of tokens in the prompt")
    completion_tokens: Optional[int] = Field(None, description="Number of tokens in the completion")
    total_tokens: Optional[int] = Field(None, description="Total number of tokens used")
    
    # Multimodal specific
    image_tokens: Optional[int] = Field(None, description="Number of tokens used for image processing")
    audio_tokens: Optional[int] = Field(None, description="Number of tokens used for audio processing")
    video_tokens: Optional[int] = Field(None, description="Number of tokens used for video processing")
    
    # Metadata
    response_id: Optional[str] = Field(None, description="Unique identifier for the response")
    raw_response: Optional[Dict[str, Any]] = Field(None, description="Original raw response")
    
    class Config:
        extra = "allow"
        use_enum_values = True
    
    @computed_field
    @property
    def provider(self) -> str:
        """Determine the provider based on the class type"""
        return self.__class__.__name__.replace("Response", "")
    
    @computed_field
    @property
    def is_multimodal(self) -> bool:
        """Check if response contains multimodal content"""
        if not self.content_parts:
            return False
        return any(part.type != ModalityType.TEXT for part in self.content_parts)
    
    @computed_field
    @property
    def modalities(self) -> List[str]:
        """List all modalities present in the response"""
        if not self.content_parts:
            return [ModalityType.TEXT.value]
        return list(set(part.type.value for part in self.content_parts))