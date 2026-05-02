import time
from maticlib.observability.trace import StepTrace, PipelineTrace

def test_step_trace():
    step = StepTrace(step_name="test_step")
    time.sleep(0.01)
    step.end_time = time.time()
    
    assert step.duration > 0
    step.prompt_tokens = 10
    step.completion_tokens = 5
    step.total_tokens = 15
    assert step.total_tokens == 15

def test_pipeline_trace_aggregation():
    pipeline = PipelineTrace(pipeline_name="test_pipeline")
    
    step1 = StepTrace(step_name="step1", prompt_tokens=10, completion_tokens=5, total_tokens=15)
    step2 = StepTrace(step_name="step2", prompt_tokens=20, completion_tokens=10, total_tokens=30)
    
    pipeline.add_step(step1)
    pipeline.add_step(step2)
    
    assert pipeline.total_prompt_tokens == 30
    assert pipeline.total_completion_tokens == 15
    assert pipeline.grand_total_tokens == 45
