from maticlib.core.formatting.sql_result import format_as_markdown_table
from maticlib.core.evaluation.evaluator import (
    ContextRelevanceEvaluator,
    AnswerAccuracyEvaluator,
)


def example_evaluation_and_formatting():
    print("--- 1. Markdown Formatting of SQL Output ---")
    columns = ["user_id", "email", "subscription_tier"]
    rows = [
        (101, "alice@example.com", "premium"),
        (102, "bob@example.com", "free"),
        (103, "charlie@example.com", "premium"),
    ]

    table_md = format_as_markdown_table(columns, rows)
    print("\nFormatted Table Output:\n")
    print(table_md)
    print("-" * 50)

    print("\n--- 2. Light Evaluator (Fallback mode) ---")
    # Evaluating Context Relevance without an LLM
    context_eval = ContextRelevanceEvaluator()
    question = "How many premium users do we have?"
    contexts = ["We have 2 premium users.", "Alice and Charlie are premium."]

    relevance = context_eval.evaluate(question, contexts)
    print(f"\nQuestion: {question}")
    print(f"Context Relevance Score: {relevance.score} ({relevance.reason})")

    # Evaluating Answer Accuracy
    answer_eval = AnswerAccuracyEvaluator()
    ground_truth = "We have exactly two premium subscribers."
    generated_answer = "We have 2 premium users."

    accuracy = answer_eval.evaluate(generated_answer, ground_truth)
    print(f"\nGenerated Answer: {generated_answer}")
    print(f"Answer Accuracy Score: {accuracy.score} ({accuracy.reason})")


if __name__ == "__main__":
    example_evaluation_and_formatting()
