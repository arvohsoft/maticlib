import json
import re
from typing import Any, Dict
from maticlib.core.parsers.base import BaseResponseParser


class JSONResponseParser(BaseResponseParser[Dict[str, Any]]):
    """
    Parses LLM output into a JSON/dictionary format.

    Includes robust extraction logic to find JSON blocks even if the model
    returns conversational text surrounding the JSON.
    """

    @staticmethod
    def _extract_json_string(text: str) -> str:
        """
        Extracts a JSON-looking string from text, handling markdown blocks.
        """
        # 1. Try to find regex extraction of JSON blocks (```json ... ```)
        json_match = re.search(
            r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL | re.IGNORECASE
        )
        if json_match:
            return json_match.group(1)

        # 2. Try finding anything between braces
        brace_match = re.search(r"(\{.*\})", text, re.DOTALL)
        if brace_match:
            return brace_match.group(1)

        return text.strip()

    def parse(self, text: str) -> Dict[str, Any]:
        """
        Parses text into a dictionary. Handles markdown formatting.
        """
        json_str = self._extract_json_string(text)
        try:
            return json.loads(json_str)
        except json.JSONDecodeError:
            raise ValueError(f"Could not parse response as JSON: {text}")

    def get_structure_instructions(self) -> str:
        """
        Instructions for JSON output.
        """
        return (
            "The output should be a valid JSON object. "
            "Do not include any conversational text or explanations outside the JSON block."
        )
