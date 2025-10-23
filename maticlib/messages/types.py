from enum import Enum

class MessageType(Enum):
    SystemMessage = 0
    HumanMessage = 1
    AIMessage = 2