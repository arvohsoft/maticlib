from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
import uuid

class TextSegment(BaseModel):
    content: str = Field(description="The chunked text snippet.")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Arbitrary metadata.")
    segment_id: str = Field(default_factory=lambda: uuid.uuid4().hex[:12], description="Unique chunk/node identifier.")

class ContextNode(BaseModel):
    segment: TextSegment
    parent_id: Optional[str] = None
    children_ids: list[str] = Field(default_factory=list)
