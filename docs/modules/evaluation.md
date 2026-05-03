# :material-checkbox-marked-circle-outline: Evaluation (`maticlib.core.evaluation`)

Modules for testing and quantifying the performance of RAG and Text2SQL pipelines.

```python
from maticlib.core.evaluation import ContextRelevanceEvaluator, AnswerAccuracyEvaluator

# Evaluate Context Relevance
context_eval = ContextRelevanceEvaluator()
relevance = context_eval.evaluate(
    question="What is the capital of France?",
    contexts=["The capital of France is Paris."]
)
print(f"Score: {relevance.score} ({relevance.reason})")

# Evaluate Answer Accuracy
accuracy_eval = AnswerAccuracyEvaluator()
accuracy = accuracy_eval.evaluate(
    answer="We have 2 premium users.",
    ground_truth="We have exactly two premium subscribers."
)
print(f"Accuracy Score: {accuracy.score}")
```
