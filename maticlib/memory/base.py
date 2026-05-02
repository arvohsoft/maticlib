from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from maticlib.messages import BaseMessage

class BaseMemory(ABC):
    @abstractmethod
    def add_message(self, message: BaseMessage) -> None:
        """Add a single message to memory."""
        pass

    @abstractmethod
    def add_messages(self, messages: List[BaseMessage]) -> None:
        """Add multiple messages to memory."""
        pass

    @abstractmethod
    def get_messages(self) -> List[BaseMessage]:
        """Retrieve the current memory context."""
        pass

    @abstractmethod
    def clear(self) -> None:
        """Clear the memory."""
        pass

    @property
    @abstractmethod
    def token_count(self) -> int:
        """Estimate of the tokens currently held in memory."""
        pass
