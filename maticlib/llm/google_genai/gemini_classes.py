# ============================================================================
# GEMINI SPECIFIC CLASSES
# ============================================================================

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from maticlib.llm.classes.client_output_model import ContentPart, LLMResponseBase, ModalityType

class GeminiPart(BaseModel):
    """Gemini content part - supports multimodal content"""
    text: Optional[str] = None
    inline_data: Optional[Dict[str, Any]] = None  # {mime_type: str, data: str}
    file_data: Optional[Dict[str, Any]] = None     # {mime_type: str, file_uri: str}
    video_metadata: Optional[Dict[str, Any]] = None
    
    class Config:
        extra = "allow"


class GeminiContent(BaseModel):
    """Gemini content structure"""
    parts: List[GeminiPart]
    role: str


class GeminiCandidate(BaseModel):
    """Gemini candidate structure"""
    content: GeminiContent
    finishReason: str
    index: int
    safety_ratings: Optional[List[Dict[str, Any]]] = None
    
    class Config:
        extra = "allow"


class GeminiPromptTokenDetail(BaseModel):
    """Gemini prompt token detail"""
    modality: str
    tokenCount: int


class GeminiUsageMetadata(BaseModel):
    """Gemini-specific usage metadata - supports multimodal tokens"""
    promptTokenCount: int
    candidatesTokenCount: int
    totalTokenCount: int
    promptTokensDetails: Optional[List[GeminiPromptTokenDetail]] = None
    thoughtsTokenCount: Optional[int] = None
    # Cached content tokens (for context caching)
    cachedContentTokenCount: Optional[int] = None


class GeminiResponse(LLMResponseBase):
    """
    Gemini-specific response structure.
    
    Supports multimodal inputs (text, image, audio, video) and outputs.
    Inherits from LLMResponseBase and adds Gemini-specific fields.
    """
    
    responseId: str = Field(..., description="Unique identifier for the Gemini response")
    modelVersion: str = Field(..., description="Gemini model version")
    candidates: List[GeminiCandidate] = Field(..., description="List of candidate responses")
    usageMetadata: GeminiUsageMetadata = Field(..., description="Token usage metadata")
    
    def __init__(self, **data):
        # Extract common fields from Gemini structure
        if 'candidates' in data and len(data['candidates']) > 0:
            first_candidate = data['candidates'][0]
            parts = first_candidate.get('content', {}).get('parts', [])
            
            if parts:
                content_parts = []
                text_parts = []
                
                for part in parts:
                    if isinstance(part, dict):
                        # Determine modality type
                        modality = ModalityType.TEXT
                        content_part = ContentPart(type=modality)
                        
                        # Extract text
                        if part.get('text'):
                            text_parts.append(part['text'])
                            content_part.text = part['text']
                        
                        # Extract inline data (images, audio, etc.)
                        if part.get('inline_data'):
                            inline = part['inline_data']
                            mime_type = inline.get('mime_type', '')
                            content_part.inline_data = inline
                            
                            if 'image' in mime_type:
                                modality = ModalityType.IMAGE
                            elif 'audio' in mime_type:
                                modality = ModalityType.AUDIO
                            elif 'video' in mime_type:
                                modality = ModalityType.VIDEO
                        
                        # Extract file data
                        if part.get('file_data'):
                            file_data = part['file_data']
                            mime_type = file_data.get('mime_type', '')
                            
                            if 'image' in mime_type:
                                modality = ModalityType.IMAGE
                                content_part.image_url = file_data.get('file_uri')
                            elif 'audio' in mime_type:
                                modality = ModalityType.AUDIO
                                content_part.audio_url = file_data.get('file_uri')
                            elif 'video' in mime_type:
                                modality = ModalityType.VIDEO
                                content_part.video_url = file_data.get('file_uri')
                        
                        content_part.type = modality
                        content_parts.append(content_part)
                
                data['content_parts'] = content_parts
                data['content'] = ' '.join(text_parts) if text_parts else None
            
            data['finish_reason'] = first_candidate.get('finishReason')
        
        # Extract token usage with multimodal support
        if 'usageMetadata' in data:
            usage = data['usageMetadata']
            data['prompt_tokens'] = usage.get('promptTokenCount')
            data['completion_tokens'] = usage.get('candidatesTokenCount')
            data['total_tokens'] = usage.get('totalTokenCount')
            
            # Parse modality-specific tokens from promptTokensDetails
            if usage.get('promptTokensDetails'):
                for detail in usage['promptTokensDetails']:
                    modality = detail.get('modality', '').lower()
                    token_count = detail.get('tokenCount', 0)
                    
                    if 'image' in modality:
                        data['image_tokens'] = token_count
                    elif 'audio' in modality:
                        data['audio_tokens'] = token_count
                    elif 'video' in modality:
                        data['video_tokens'] = token_count
        
        # Set response_id and model
        data['response_id'] = data.get('responseId')
        data['model'] = data.get('modelVersion', 'gemini')
        
        # Store raw response
        data['raw_response'] = data.copy()
        
        super().__init__(**data)
    
    @property
    def thoughts_token_count(self) -> Optional[int]:
        """Get the thoughts token count if available (Gemini-specific)"""
        return self.usageMetadata.thoughtsTokenCount
    
    @property
    def cached_token_count(self) -> Optional[int]:
        """Get cached content token count (Gemini context caching)"""
        return self.usageMetadata.cachedContentTokenCount