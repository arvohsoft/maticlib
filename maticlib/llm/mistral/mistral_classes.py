from datetime import datetime
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field, computed_field

from maticlib.llm.classes.client_output import ContentPart, LLMResponseBase, ModalityType

# ============================================================================
# MISTRAL SPECIFIC CLASSES
# ============================================================================

class MistralUsage(BaseModel):
    """Mistral-specific usage information"""
    prompt_tokens: int
    total_tokens: int
    completion_tokens: int
    # Multimodal token counts (if available)
    image_tokens: Optional[int] = None
    audio_tokens: Optional[int] = None
    video_tokens: Optional[int] = None


class MistralContentPart(BaseModel):
    """Mistral content part - can be text or multimodal"""
    type: str = Field(default="text")
    text: Optional[str] = None
    image_url: Optional[Union[str, Dict[str, str]]] = None
    
    class Config:
        extra = "allow"


class MistralMessage(BaseModel):
    """Mistral message structure - supports multimodal content"""
    role: str
    content: Optional[Union[str, List[MistralContentPart]]] = None
    tool_calls: Optional[Any] = None


class MistralChoice(BaseModel):
    """Mistral choice structure"""
    index: int
    finish_reason: str
    message: MistralMessage


class MistralResponse(LLMResponseBase):
    """
    Mistral-specific response structure.
    
    Supports both text-only and multimodal (Pixtral) models.
    Inherits from LLMResponseBase and adds Mistral-specific fields.
    """
    
    id: str = Field(..., description="Unique identifier for the Mistral response")
    created: int = Field(..., description="Unix timestamp of creation")
    object: str = Field(..., description="Object type (e.g., 'chat.completion')")
    choices: List[MistralChoice] = Field(..., description="List of completion choices")
    usage: MistralUsage = Field(..., description="Token usage information")
    
    def __init__(self, **data):
        # Extract common fields from Mistral structure
        if 'choices' in data and len(data['choices']) > 0:
            first_choice = data['choices'][0]
            message = first_choice.get('message', {})
            content = message.get('content')
            
            # Handle multimodal content (list of parts) or text-only (string)
            if isinstance(content, list):
                # Multimodal response with parts
                content_parts = []
                text_parts = []
                for part in content:
                    if isinstance(part, dict):
                        content_part = ContentPart(
                            type=ModalityType(part.get('type', 'text')),
                            text=part.get('text'),
                            image_url=part.get('image_url'),
                        )
                        content_parts.append(content_part)
                        if part.get('text'):
                            text_parts.append(part['text'])
                
                data['content_parts'] = content_parts
                data['content'] = ' '.join(text_parts) if text_parts else None
            else:
                # Simple text response
                data['content'] = content
                if content:
                    data['content_parts'] = [ContentPart(type=ModalityType.TEXT, text=content)]
            
            data['finish_reason'] = first_choice.get('finish_reason')
        
        # Extract token usage
        if 'usage' in data:
            usage = data['usage']
            data['prompt_tokens'] = usage.get('prompt_tokens')
            data['completion_tokens'] = usage.get('completion_tokens')
            data['total_tokens'] = usage.get('total_tokens')
            data['image_tokens'] = usage.get('image_tokens')
            data['audio_tokens'] = usage.get('audio_tokens')
            data['video_tokens'] = usage.get('video_tokens')
        
        # Set response_id and model
        data['response_id'] = data.get('id')
        
        # Store raw response
        data['raw_response'] = data.copy()
        
        super().__init__(**data)
    
    @computed_field
    @property
    def timestamp(self) -> datetime:
        """Convert Unix timestamp to datetime"""
        return datetime.fromtimestamp(self.created)