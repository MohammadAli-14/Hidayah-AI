"""
Hidayah AI — Text Sanitization
Centralises HTML escaping and text cleaning for all UI rendering.
"""

from html import escape as _html_escape


def escape_html(text: str) -> str:
    """Escape HTML entities in text for safe rendering inside HTML templates.

    Converts &, <, >, ", ' to their HTML entity equivalents.
    Returns empty string for None/falsy input.
    """
    if not text:
        return ""
    return _html_escape(str(text), quote=True)


def truncate(text: str, max_length: int = 500, suffix: str = "…") -> str:
    """Truncate text to max_length characters, appending suffix if shortened."""
    if not text or len(text) <= max_length:
        return text or ""
    return text[:max_length].rstrip() + suffix


def clean_excerpt(text: str, max_length: int = 2000) -> str:
    """Clean and truncate an excerpt for display — strips whitespace, truncates."""
    cleaned = (text or "").strip()
    return truncate(cleaned, max_length)
