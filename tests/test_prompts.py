import pytest
from maticlib.prompts.base import BasePromptTemplate
from maticlib.prompts.registry import PromptRegistry
from maticlib.exceptions import TemplateRenderError

def test_prompt_template_formatting():
    template = BasePromptTemplate(template="Hello {name}, your score is {score}.")
    
    # Auto-detected variables
    assert set(template.input_variables) == {"name", "score"}
    
    result = template.format(name="Alice", score=100)
    assert result == "Hello Alice, your score is 100."

def test_prompt_template_missing_vars():
    template = BasePromptTemplate(template="Hello {name}")
    with pytest.raises(TemplateRenderError):
        template.format() # Missing 'name'

def test_prompt_registry():
    rag_prompt = PromptRegistry.get("rag_qa")
    assert "{context}" in rag_prompt.template
    assert "{question}" in rag_prompt.template
