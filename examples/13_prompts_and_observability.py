from maticlib.prompts.registry import PromptRegistry
from maticlib.observability.trace import PipelineTrace, StepTrace
from maticlib.observability.callbacks import LoggingCallbackHandler
from maticlib.resilience.retry import with_retry
from maticlib.memory.buffer import WindowBufferMemory
from maticlib.messages import HumanMessage, AIMessage
import time
import logging

# Configure basic logging so we can see the observability callbacks in the console
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def example_prompts_and_memory():
    print("--- 1. Using Prompt Registry and Memory ---")

    # Get a built-in RAG prompt template
    prompt_template = PromptRegistry.get("rag_qa")
    formatted_prompt = prompt_template.format(
        context="Maticlib is a powerful agentic automation library.",
        question="What is Maticlib?",
    )
    print("Formatted Prompt:\n", formatted_prompt)

    # Store the interaction in a rolling window memory buffer
    memory = WindowBufferMemory(k=5)
    memory.add_message(HumanMessage(content=formatted_prompt))
    memory.add_message(
        AIMessage(content="Maticlib is a powerful agentic automation library.")
    )

    print(f"Memory contains {len(memory.get_messages())} messages.")
    print(f"Estimated tokens in memory context: {memory.token_count}\n")


@with_retry(max_retries=3, backoff_factor=1.5, initial_delay=0.5)
def flaky_external_call(simulate_fail=True):
    """Simulates an external API call that might fail."""
    if simulate_fail and not hasattr(flaky_external_call, "has_run"):
        flaky_external_call.has_run = True
        print("    [External API] Connection reset by peer! Failing...")
        raise ConnectionError("Network failure")
    print("    [External API] Success!")
    return "Response data"


def example_observability_and_resilience():
    print("--- 2. Observability Tracing & Resilience ---")

    handler = LoggingCallbackHandler()
    pipeline_trace = PipelineTrace(pipeline_name="Resilient_RAG_Pipeline")
    handler.on_pipeline_start(pipeline_trace)

    # Simulate Step 1: Retrieval
    step1 = StepTrace(step_name="Vector_Retrieval")
    handler.on_step_start(step1)
    time.sleep(0.1)  # Simulate work
    step1.end_time = time.time()
    step1.prompt_tokens = 25  # Simulated vector token extraction
    pipeline_trace.add_step(step1)
    handler.on_step_end(step1)

    # Simulate Step 2: Generation with Retry
    step2 = StepTrace(step_name="LLM_Generation")
    handler.on_step_start(step2)
    try:
        # This will fail the first time, wait 0.5s, then succeed
        flaky_external_call()
        step2.completion_tokens = 50
        step2.total_tokens = 50
    except Exception as e:
        step2.error = str(e)
    finally:
        step2.end_time = time.time()
        pipeline_trace.add_step(step2)
        handler.on_step_end(step2)

    pipeline_trace.end_time = time.time()
    handler.on_pipeline_end(pipeline_trace)


if __name__ == "__main__":
    example_prompts_and_memory()
    example_observability_and_resilience()
