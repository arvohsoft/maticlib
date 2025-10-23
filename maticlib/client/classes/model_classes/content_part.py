from typing import Optional, Dict, Any

from pydantic import BaseModel, Field

from maticlib.client.classes.enums.modality_type import ModalityType


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