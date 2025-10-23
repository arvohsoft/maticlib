from enum import Enum
class ModalityType(str, Enum):
    """Supported modality types"""
    TEXT = "text"
    IMAGE = "image"
    AUDIO = "audio"
    VIDEO = "video"
    UNKNOWN = "unknown"