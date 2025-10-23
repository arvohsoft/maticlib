from .types import MessageType

class BaseMessage:
    def __init__(
        self,
        content: str|None,
        message_type: str|int|MessageType
    ):
        if not isinstance(content, str):
            raise TypeError(f"Content is {type(content)}. It should be string.")
        
        self.content = content
        
        if isinstance(message_type, str):
            if message_type == MessageType.SystemMessage.name:
                self.message_type = MessageType.SystemMessage
            elif message_type == MessageType.HumanMessage.name:
                self.message_type = MessageType.HumanMessage
            elif message_type == MessageType.AIMessage.name:
                self.message_type = MessageType.AIMessage
            raise TypeError(content="")
        elif isinstance(message_type, int):
            if message_type == MessageType.SystemMessage.value:
                self.message_type = MessageType.SystemMessage
            elif message_type == MessageType.HumanMessage.value:
                self.message_type = MessageType.HumanMessage
            elif message_type == MessageType.AIMessage.value:
                self.message_type = MessageType.AIMessage
        elif isinstance(message_type, MessageType):
            self.message_type = message_type