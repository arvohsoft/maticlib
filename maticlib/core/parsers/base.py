from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

T = TypeVar("T")

class BaseResponseParser(ABC, Generic[T]):
    """
    Base class for response parsers.
    
    A response parser is responsible for:
    1. Providing structural instructions to the LLM.
    2. Parsing the LLM's text output into a structured object.
    """
    
    @abstractmethod
    def parse(self, text: str) -> T:
        """
        Parses the raw text output from an LLM.
        
        Args:
            text (str): The raw text response from the model.
            
        Returns:
            T: The parsed structured object.
        """
        pass
        
    @abstractmethod
    def get_structure_instructions(self) -> str:
        """
        Provides instructions to the LLM on how to structure its output.
        
        Returns:
            str: Formatting instructions for the prompt.
        """
        pass
