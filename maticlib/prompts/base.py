from typing import Dict, Any, List
from string import Formatter
from pydantic import BaseModel, Field
from maticlib.exceptions import TemplateRenderError

class BasePromptTemplate(BaseModel):
    """
    A simple, Pydantic-backed prompt template with auto-detected input variables.

    Attributes:
        template: The string template with ``{variable}`` placeholders.
        input_variables: List of expected variable names. Auto-detected from
            the template if not provided.
    """

    template: str
    input_variables: List[str] = Field(default_factory=list)

    def __init__(self, **data: Any):
        """
        Initializes the BasePromptTemplate.

        Args:
            **data: Pydantic field values. Accepts ``template`` (str) and
                optionally ``input_variables`` (list[str]).
        """
        super().__init__(**data)
        if not self.input_variables:
            self.input_variables = [
                fname for _, fname, _, _ in Formatter().parse(self.template) if fname
            ]

    def format(self, **kwargs: Any) -> str:
        """
        Renders the template by filling all named variables.

        Args:
            **kwargs: Keyword arguments matching the template's input_variables.

        Returns:
            The fully rendered prompt string.

        Raises:
            TemplateRenderError: If a required variable is missing.
        """
        missing = set(self.input_variables) - set(kwargs.keys())
        if missing:
            raise TemplateRenderError(f"Missing required input variables: {missing}")
        try:
            return self.template.format(**kwargs)
        except KeyError as e:
            raise TemplateRenderError(f"Missing expected key during format: {e}")
        except Exception as e:
            raise TemplateRenderError(f"Failed to format template: {e}")

