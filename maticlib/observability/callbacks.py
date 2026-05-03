from abc import ABC, abstractmethod
import logging
from typing import Any
from maticlib.observability.trace import StepTrace, PipelineTrace


class BaseCallbackHandler(ABC):
    """Abstract base class for pipeline event callbacks."""

    @abstractmethod
    def on_step_start(self, step: StepTrace) -> None:
        """
        Called when a pipeline step begins.

        Args:
            step: The StepTrace for the starting step.
        """
        pass

    @abstractmethod
    def on_step_end(self, step: StepTrace) -> None:
        """
        Called when a pipeline step ends.

        Args:
            step: The completed StepTrace.
        """
        pass

    @abstractmethod
    def on_pipeline_start(self, trace: PipelineTrace) -> None:
        """
        Called when a pipeline starts.

        Args:
            trace: The PipelineTrace for the starting pipeline.
        """
        pass

    @abstractmethod
    def on_pipeline_end(self, trace: PipelineTrace) -> None:
        """
        Called when a pipeline completes.

        Args:
            trace: The finished PipelineTrace.
        """
        pass


class LoggingCallbackHandler(BaseCallbackHandler):
    """A callback handler that logs pipeline and step events via Python's logging module."""

    def __init__(self, logger: logging.Logger = None):
        """
        Initializes the LoggingCallbackHandler.

        Args:
            logger: An optional Python Logger. Defaults to the module logger.
        """
        self.logger = logger or logging.getLogger(__name__)

    def on_step_start(self, step: StepTrace) -> None:
        self.logger.info(f"Starting step: {step.step_name} [{step.step_id}]")

    def on_step_end(self, step: StepTrace) -> None:
        status = "Failed" if step.error else "Completed"
        msg = (
            f"Step {step.step_name} {status} in {step.duration:.3f}s. "
            f"Tokens: {step.prompt_tokens} prompt + {step.completion_tokens} completion "
            f"= {step.total_tokens} total. Model: {step.model_name}"
        )
        if step.error:
            self.logger.error(f"{msg}\nError: {step.error}")
        else:
            self.logger.info(msg)

    def on_pipeline_start(self, trace: PipelineTrace) -> None:
        self.logger.info(
            f"=== Starting Pipeline: {trace.pipeline_name} [{trace.trace_id}] ==="
        )

    def on_pipeline_end(self, trace: PipelineTrace) -> None:
        self.logger.info(
            f"=== Pipeline {trace.pipeline_name} Finished in {trace.total_duration:.3f}s ===\n"
            f"Total Tokens: {trace.grand_total_tokens} "
            f"({trace.total_prompt_tokens} prompt, {trace.total_completion_tokens} completion)"
        )
