import re
import html
from fastapi import HTTPException

ALLOWED_EXTENSIONS = {".py", ".js", ".ts", ".md"}
BLOCKED_PATTERNS = [
    r"\.\.\/",          # path traversal
    r"[;&|`$]",         # shell injection chars
    r"<script",         # XSS
    r"javascript:",     # JS injection
]

def validate_repo_url(url: str) -> str:
    """
    Validates GitHub repo URL strictly.
    Returns the sanitized URL.
    Raises 400 if invalid.
    """
    if not url or not isinstance(url, str):
        raise HTTPException(status_code=400, detail="Repo URL is required")

    url = url.strip()

    # Only allow public GitHub repos with clean names
    pattern = r"^https://github\.com/[a-zA-Z0-9_\-\.]+/[a-zA-Z0-9_\-\.]+/?$"
    if not re.match(pattern, url):
        raise HTTPException(
            status_code=400,
            detail="Invalid GitHub URL. Must be: https://github.com/owner/repo"
        )

    # Check for injection attempts in the URL
    for pat in BLOCKED_PATTERNS:
        if re.search(pat, url, re.IGNORECASE):
            raise HTTPException(status_code=400, detail="Invalid characters in URL")

    # Strip trailing slash for consistency
    return url.rstrip("/")


def sanitize_query(query: str) -> str:
    """
    Sanitizes user query to prevent prompt injection.
    """
    if not query or not isinstance(query, str):
        raise HTTPException(status_code=400, detail="Query is required")

    # Strip HTML tags and escape HTML entities
    query = html.escape(query.strip())

    # Remove null bytes and control characters (keep newlines)
    query = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", "", query)

    # Soft prompt injection detection — warn but don't block
    injection_hints = [
        "ignore previous instructions",
        "ignore all instructions",
        "you are now",
        "disregard your",
        "system prompt",
        "act as",
    ]
    lower_q = query.lower()
    for hint in injection_hints:
        if hint in lower_q:
            # Log this in production; for now strip and truncate
            raise HTTPException(
                status_code=400,
                detail="Query contains disallowed patterns"
            )

    return query