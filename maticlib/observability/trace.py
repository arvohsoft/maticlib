from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
import time
import uuid


class StepTrace(BaseModel):
    """
    Captures observability data for a single pipeline step.

    Attributes:
        step_id: Unique identifier for the step.
        step_name: Human-readable name of the step.
        start_time: Unix timestamp when the step started.
        end_time: Unix timestamp when the step ended (or None if still running).
        inputs: Arbitrary input data associated with the step.
        outputs: Arbitrary output data associated with the step.
        error: Error message if the step failed.
        prompt_tokens: Number of input/prompt tokens consumed.
        completion_tokens: Number of completion tokens generated.
        total_tokens: Total tokens used (prompt + completion).
        model_name: LLM or embedding model name used in this step.
    """

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
    """
    Container that aggregates StepTrace records for a full pipeline execution.

    Attributes:
        trace_id: Unique identifier for this pipeline trace.
        pipeline_name: Human-readable name for the pipeline.
        start_time: Unix timestamp when the pipeline started.
        end_time: Unix timestamp when the pipeline ended (or None if still running).
        steps: Ordered list of StepTrace records.
        metadata: Arbitrary metadata associated with this pipeline run.
    """

    trace_id: str = Field(default_factory=lambda: uuid.uuid4().hex)
    pipeline_name: str
    start_time: float = Field(default_factory=time.time)
    end_time: Optional[float] = None
    steps: List[StepTrace] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)

    def add_step(self, step: StepTrace):
        """
        Appends a completed StepTrace to the pipeline trace.

        Args:
            step: A finished StepTrace to record.
        """
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
