# :material-chart-line: Observability & Resilience (`maticlib.observability` & `maticlib.resilience`)

### **Tracing**
Easily log execution time, token usage, and errors across the entire lifecycle.

```python
from maticlib.observability.trace import PipelineTrace
from maticlib.observability.callbacks import LoggingCallbackHandler

trace = PipelineTrace(pipeline_name="My_RAG")
handler = LoggingCallbackHandler()
handler.on_pipeline_start(trace)
# ... run steps ...
handler.on_pipeline_end(trace)
```

### **Retry Policies**
Handle flaky external LLM APIs with robust, exponential backoff.
- Use `RetryPolicy` manually or the `@with_retry(max_retries=3)` decorator on any function.

```python
from maticlib.resilience.retry import with_retry

@with_retry(max_retries=3, initial_delay=1.0)
def call_external_api():
    # Will automatically retry on exceptions
    pass
```
