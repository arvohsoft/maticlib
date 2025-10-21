from __future__ import annotations

def formatting(content: str, params: str|dict|list):
    if isinstance(params, str):
        content.format(params)
    elif isinstance(params, list):
        pass