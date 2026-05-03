import abc
from typing import Optional, List, Any
from maticlib.core.evaluation.models import EvaluationResult

class BaseEvaluator(abc.ABC):
    """
    Abstract base class for all evaluation metrics.
    Makes the evaluation module highly extensible.
    """
    @abc.abstractmethod
    def evaluate(self, **kwargs) -> EvaluationResult:
        pass


class ContextRelevanceEvaluator(BaseEvaluator):
    """
    Evaluates context relevance to a question using basic keyword/token overlap or an optional LLM.
    """
    def __init__(self, llm_client: Optional[Any] = None):
        """
        Initializes the ContextRelevanceEvaluator.

        Args:
            llm_client: Optional LLM client to use as a judge.
        """
        self.llm_client = llm_client

    def evaluate(self, question: str, contexts: List[str], **kwargs) -> EvaluationResult:
        """
        Calculates context relevance score.

        Args:
            question: The natural language question to test.
            contexts: A list of text context segments.

        Returns:
            An EvaluationResult containing score and reasoning.
        """
        if not contexts:
            return EvaluationResult(
                metric_name="context_relevance",
                score=0.0,
                reason="No contexts provided for evaluation."
            )
            
        context_text = " ".join(contexts)
        
        # If no LLM client is available, fallback to fuzzy/token overlap matching
        if not self.llm_client:
            q_words = set(w.lower() for w in question.split() if len(w) > 3)
            if not q_words:
                return EvaluationResult(
                    metric_name="context_relevance",
                    score=1.0,
                    reason="Question too short to extract meaningful evaluation words."
                )
            
            c_words = set(w.lower() for w in context_text.split())
            matches = q_words.intersection(c_words)
            score = len(matches) / len(q_words)
            return EvaluationResult(
                metric_name="context_relevance",
                score=round(score, 2),
                reason=f"Keyword overlap fallback. Found {len(matches)} out of {len(q_words)} question terms."
            )
            
        # Use LLM-as-a-judge
        prompt = (
            f"Evaluate the relevance of the following retrieved contexts to the question.\n"
            f"Assign a score between 0.0 and 1.0 (1.0 = highly relevant, 0.0 = completely irrelevant).\n"
            f"Output only the numeric score on the first line, followed by your reasoning on the next line.\n"
            f"Question: {question}\n"
            f"Contexts:\n{context_text}"
        )
        try:
            res = self.llm_client.complete(prompt)
            raw = self.llm_client.get_text_response(res).strip()
            lines = [line.strip() for line in raw.split("\n") if line.strip()]
            score = float(lines[0])
            reason = lines[1] if len(lines) > 1 else "LLM evaluation successful."
            return EvaluationResult(
                metric_name="context_relevance",
                score=min(max(score, 0.0), 1.0),
                reason=reason
            )
        except Exception as e:
            return EvaluationResult(
                metric_name="context_relevance",
                score=0.0,
                reason=f"LLM evaluation failed: {e}"
            )


class AnswerAccuracyEvaluator(BaseEvaluator):
    """
    Evaluates answer accuracy by comparing against a ground truth answer.
    """
    def __init__(self, llm_client: Optional[Any] = None):
        """
        Initializes the AnswerAccuracyEvaluator.

        Args:
            llm_client: Optional LLM client to use as a judge.
        """
        self.llm_client = llm_client

    def evaluate(self, answer: str, ground_truth: str, **kwargs) -> EvaluationResult:
        """
        Calculates answer accuracy against ground truth.

        Args:
            answer: Generated text answer string.
            ground_truth: Ground truth reference text answer string.

        Returns:
            An EvaluationResult containing score and reasoning.
        """
        if not ground_truth:
            return EvaluationResult(
                metric_name="answer_accuracy",
                score=0.0,
                reason="No ground truth provided."
            )
            
        if not self.llm_client:
            # Fallback to simple token similarity or string exact match
            if answer.strip().lower() == ground_truth.strip().lower():
                return EvaluationResult(
                    metric_name="answer_accuracy",
                    score=1.0,
                    reason="Exact match."
                )
                
            ans_words = set(w.lower() for w in answer.split())
            gt_words = set(w.lower() for w in ground_truth.split())
            if not gt_words:
                return EvaluationResult(
                    metric_name="answer_accuracy",
                    score=0.0,
                    reason="Ground truth had no significant terms."
                )
                
            overlap = ans_words.intersection(gt_words)
            score = len(overlap) / len(gt_words)
            return EvaluationResult(
                metric_name="answer_accuracy",
                score=round(score, 2),
                reason=f"Word matching fallback. Matches: {len(overlap)}/{len(gt_words)}"
            )
            
        # Use LLM-as-a-judge
        prompt = (
            f"Grade the generated answer against the reference ground truth answer.\n"
            f"Does the generated answer convey the same core facts and details?\n"
            f"Assign a score between 0.0 and 1.0 (1.0 = completely accurate, 0.0 = completely wrong).\n"
            f"Output only the numeric score on the first line, followed by your reasoning on the next line.\n"
            f"Generated Answer: {answer}\n"
            f"Ground Truth Answer: {ground_truth}"
        )
        try:
            res = self.llm_client.complete(prompt)
            raw = self.llm_client.get_text_response(res).strip()
            lines = [line.strip() for line in raw.split("\n") if line.strip()]
            score = float(lines[0])
            reason = lines[1] if len(lines) > 1 else "LLM accuracy assessment completed."
            return EvaluationResult(
                metric_name="answer_accuracy",
                score=min(max(score, 0.0), 1.0),
                reason=reason
            )
        except Exception as e:
            return EvaluationResult(
                metric_name="answer_accuracy",
                score=0.0,
                reason=f"LLM accuracy check failed: {e}"
            )
