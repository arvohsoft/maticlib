from enum import Enum


class RoleType(str, Enum):
    """Role types in conversation"""
    USER = "user"
    ASSISTANT = "assistant"
    MODEL = "model"
    SYSTEM = "system"