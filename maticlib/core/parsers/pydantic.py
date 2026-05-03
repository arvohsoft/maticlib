import json
from typing import Type, TypeVar, Generic
from pydantic import BaseModel
from maticlib.core.parsers.base import BaseResponseParser
from maticlib.core.parsers.json import JSONResponseParser

T = TypeVar("T", bound=BaseModel)


class PydanticResponseParser(BaseResponseParser[T], Generic[T]):
    """
    Parses LLM output into a specific Pydantic model.

    Ensures that the response not only conforms to JSON but matches the
    expected schema and types defined by the Pydantic model.
    """

    def __init__(self, model: Type[T]):
        self.model = model

    def parse(self, text: str) -> T:
        """
        Parses text into a Pydantic model instance.
        """
        # Use the reusable extraction logic from JSONResponseParser
        json_str = JSONResponseParser._extract_json_string(text)

        try:
            raw_dict = json.loads(json_str)
            return self.model.model_validate(raw_dict)
        except (json.JSONDecodeError, Exception) as e:
            raise ValueError(
                f"Could not parse or validate response as Pydantic model: {e}"
            )

    def get_structure_instructions(self) -> str:
        """
        Generates instructions based on the Pydantic model schema.
        """
        schema = self.model.model_json_schema()
        # Simplify schema for the prompt
        essential_schema = {
            k: v for k, v in schema.items() if k in ["properties", "required", "type"]
        }

        return (
            f"The output should be a valid JSON object matching this schema: {json.dumps(essential_schema)}\n"
            "Respond strictly with the JSON object and no other text."
        )
