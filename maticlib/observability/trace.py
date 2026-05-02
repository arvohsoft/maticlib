from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
import time
import uuid

class StepTrace(BaseModel):
    step_id: str = Field(default_factory=lambda: uuid.uuid4().hex[:12])
    step_name: str
    start_time: float = Field(default_factory=time.time)
    end_time: Optional[float] = None
    inputs: Dict[str, Any] = Field(default_factory=dict)
    outputs: Dict[str, Any] = Field(default_factory=dict)
    error: Optional[str] = None
    
    # Token usage specifically extracted from Embeddings and LLMs
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    model_name: Optional[str] = None

    @property
    def duration(self) -> float:
        if self.end_time:
            return self.end_time - self.start_time
        return time.time() - self.start_time

class PipelineTrace(BaseModel):
    trace_id: str = Field(default_factory=lambda: uuid.uuid4().hex)
    pipeline_name: str
    start_time: float = Field(default_factory=time.time)
    end_time: Optional[float] = None
    steps: List[StepTrace] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)

    def add_step(self, step: StepTrace):
        self.steps.append(step)

    @property
    def total_duration(self) -> float:
        if self.end_time:
            return self.end_time - self.start_time
        return time.time() - self.start_time
    
    @property
    def total_prompt_tokens(self) -> int:
        return sum(s.prompt_tokens for s in self.steps)

    @property
    def total_completion_tokens(self) -> int:
        return sum(s.completion_tokens for s in self.steps)

    @property
    def grand_total_tokens(self) -> int:
        return sum(s.total_tokens for s in self.steps)
