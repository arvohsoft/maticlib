from __future__ import annotations
from .types import MessageType
from .message import BaseMessage

class AIMessage(BaseMessage):
    def __init__(self, content: str):
        if isinstance(content, str):
            super().__init__(content=content, message_type=MessageType.AIMessage)
        else:
            raise TypeError(f"Content is {type(content)}. It should be string")