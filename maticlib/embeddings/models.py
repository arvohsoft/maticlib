from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class EmbedQueryResponse(BaseModel):
    vector: List[float] = Field(description="The high-dimensional vector for the query.")
    prompt_tokens: int = Field(default=0, description="Tokens consumed by the input prompt.")
    total_tokens: int = Field(default=0, description="Total tokens consumed.")
    model: str = Field(default="", description="The specific model ID used by the provider.")
    raw_response: Optional[Dict[str, Any]] = Field(default=None, description="The original raw response from the provider.")

class EmbedDocumentsResponse(BaseModel):
    vectors: List[List[float]] = Field(description="The list of vectors for the documents.")
    prompt_tokens: int = Field(default=0, description="Tokens consumed by the input prompt.")
    total_tokens: int = Field(default=0, description="Total tokens consumed.")
    model: str = Field(default="", description="The specific model ID used by the provider.")
    raw_response: Optional[Dict[str, Any]] = Field(default=None, description="The original raw response from the provider.")
