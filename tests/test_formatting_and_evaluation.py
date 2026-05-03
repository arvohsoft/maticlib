from maticlib.core.formatting.sql_result import format_as_markdown_table
from maticlib.core.evaluation.evaluator import (
    ContextRelevanceEvaluator,
    AnswerAccuracyEvaluator,
)


def test_markdown_formatting():
    cols = ["id", "name"]
    rows = [(1, "Alice"), (2, "Bob")]

    md = format_as_markdown_table(cols, rows)
    assert "| id | name |" in md
    assert "| 1 | Alice |" in md
    assert "| 2 | Bob |" in md


def test_context_relevance_evaluator_fallback():
    evaluator = ContextRelevanceEvaluator()
    question = "What is the capital of France?"
    contexts = ["The capital of France is Paris.", "Paris is beautiful."]

    res = evaluator.evaluate(question, contexts)
    print("REASON WAS:", res.reason)
    assert res.metric_name == "context_relevance"
    assert res.score > 0.0
    assert "keyword" in res.reason.lower()


def test_answer_accuracy_evaluator_fallback():
    evaluator = AnswerAccuracyEvaluator()

    res = evaluator.evaluate("Apple pie is sweet.", "Apple pie is sweet.")
    assert res.metric_name == "answer_accuracy"
    assert res.score == 1.0
    assert "exact match" in res.reason.lower()
