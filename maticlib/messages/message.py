from .types import MessageType


class BaseMessage:
    """
    Base class for all message types in the library.

    Acts as a container for message content and metadata about the message role.

    Attributes:
        content (str): The text content of the message.
        message_type (MessageType): The enum type of the message (System, Human, AI).
    """

    def __init__(self, content: str | None, message_type: str | int | MessageType):
        """
        Initializes a new message.

        Args:
            content (str | None): The string content of the message.
            message_type (str | int | MessageType): The role/type of the message.

        Raises:
            TypeError: If content is not a string or if message_type handling fails.
        """
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
