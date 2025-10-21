from .types import MessageType
from .message import BaseMessage

class SystemMessage(BaseMessage):
    def __init__(self, content):
        if isinstance(content, str):
            super().__init__(content=content, message_type=MessageType.SystemMessage)
        else:
            raise TypeError(f"Content is {type(content)}. It should be string")