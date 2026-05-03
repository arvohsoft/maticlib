from typing import Optional, Dict, Any
from pydantic import BaseModel

class EvaluationResult(BaseModel):
    """
    Standardized schema returned by all evaluators.
    """
    metric_name: str
    score: float
    reason: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
