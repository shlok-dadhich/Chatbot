"""
frontend/utils.py
-----------------
Pure helper functions used by the Streamlit app.
No Streamlit imports here — keeping this testable and import-safe.
"""

from __future__ import annotations

import re
import uuid
from typing import Any


def generate_thread_id() -> str:
    """Return a fresh UUID string for a new conversation thread."""
    return str(uuid.uuid4())


def content_to_text(content: Any) -> str:
    """Normalise LangChain message content to a plain string for rendering."""
    if content is None:
        return ""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for item in content:
            if isinstance(item, str) and item.strip():
                parts.append(item)
            elif isinstance(item, dict):
                text = item.get("text") or item.get("content")
                if isinstance(text, str) and text.strip():
                    parts.append(text)
        return "".join(parts)
    if isinstance(content, dict):
        text = content.get("text") or content.get("content")
        return text if isinstance(text, str) else ""
    return ""


def strip_memory_json(text: str) -> str:
    """Remove any leaked MemoryDecision JSON that may appear at the start of AI output."""
    if not text:
        return ""
    pattern = r'^\s*\{"should_write"\s*:\s*(?:true|false)\s*,\s*"memories"\s*:\s*\[[\s\S]*?\]\}\s*'
    return re.sub(pattern, "", text, count=1, flags=re.IGNORECASE)


def get_view_mode(query_params: dict) -> str:
    """Extract the ?view= query-param value, defaulting to 'chat'."""
    view = query_params.get("view", "chat")
    return (view[0] if isinstance(view, list) else view) or "chat"
