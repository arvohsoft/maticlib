from __future__ import annotations

class MessageTypeError(ExceptionGroup):
    def __init__(self, message, exceptions):
        super().__init__(message, exceptions)
    
    def __call__(self, *args, **kwds):
        return super().__call__(*args, **kwds)