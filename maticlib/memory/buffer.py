from typing import List, Dict, Any, Optional
from maticlib.messages import BaseMessage
from maticlib.memory.base import BaseMemory


class ConversationBufferMemory(BaseMemory):
    """Stores all conversation messages in a sequential buffer."""

    def __init__(self, return_messages: bool = True):
        """
        Initializes ConversationBufferMemory.

        Args:
            return_messages: If True, returns the full list of BaseMessage objects.
        """
        self.messages: List[BaseMessage] = []
        self.return_messages = return_messages

    def add_message(self, message: BaseMessage) -> None:
        self.messages.append(message)

    def add_messages(self, messages: List[BaseMessage]) -> None:
        self.messages.extend(messages)

    def get_messages(self) -> List[BaseMessage]:
        return self.messages

    def clear(self) -> None:
        self.messages = []

    @property
    def token_count(self) -> int:
        # A simple heuristic since actual tokens depend on the model tokenizer
        # Assuming ~4 characters per token as a rough fallback
        total_chars = sum(len(str(m.content)) for m in self.messages if m.content)
        return total_chars // 4


class WindowBufferMemory(ConversationBufferMemory):
    """Keeps only the most recent `k` messages (sliding window)."""

    def __init__(self, k: int = 10, return_messages: bool = True):
        """
        Initializes WindowBufferMemory.

        Args:
            k: Maximum number of recent messages to retain. Default is 10.
            return_messages: If True, returns BaseMessage objects.
        """
        super().__init__(return_messages)
        self.k = k

    def get_messages(self) -> List[BaseMessage]:
        return self.messages[-self.k :] if self.k > 0 else []

    @property
    def token_count(self) -> int:
        active_messages = self.get_messages()
        total_chars = sum(len(str(m.content)) for m in active_messages if m.content)
        return total_chars // 4
