from typing import Dict, Any, List
from string import Formatter
from pydantic import BaseModel, Field
from maticlib.exceptions import TemplateRenderError

class BasePromptTemplate(BaseModel):
    template: str
    input_variables: List[str] = Field(default_factory=list)

    def __init__(self, **data):
        super().__init__(**data)
        if not self.input_variables:
            self.input_variables = [
                fname for _, fname, _, _ in Formatter().parse(self.template) if fname
            ]

    def format(self, **kwargs) -> str:
        missing = set(self.input_variables) - set(kwargs.keys())
        if missing:
            raise TemplateRenderError(f"Missing required input variables: {missing}")
        try:
            return self.template.format(**kwargs)
        except KeyError as e:
            raise TemplateRenderError(f"Missing expected key during format: {e}")
        except Exception as e:
            raise TemplateRenderError(f"Failed to format template: {e}")
