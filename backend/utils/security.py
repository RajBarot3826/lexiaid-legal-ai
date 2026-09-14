"""Security utilities for LexiAid.

Provides input sanitization, prompt-injection detection, rate limiting,
and ethical disclaimer generation for the legal analysis platform.
"""

import logging
import re
import time
from collections import defaultdict
from typing import Final, Tuple

logger: logging.Logger = logging.getLogger("lexiaid.security")

# ---------------------------------------------------------------------------
# Ethical / Legal Disclaimer
# ---------------------------------------------------------------------------
DISCLAIMER_TEXT: Final[str] = (
    "STATUTORY LEGAL NOTICE & ETHICAL DISCLAIMER: LexiAid is an artificial intelligence "
    "informational tool designed to help users read, understand, and organize legal documents. "
    "LexiAid does not provide formal legal advice, does not practice law, and does not create an "
    "attorney-client relationship. For binding legal representation or specific legal actions, "
    "always consult a licensed attorney or legal advocate in your jurisdiction."
)

# ---------------------------------------------------------------------------
# Prompt-Injection Detection Patterns
# ---------------------------------------------------------------------------
SUSPICIOUS_PATTERNS: Final[list[str]] = [
    r"ignore\s+(all\s+)?(previous|prior)\s+instructions",
    r"disregard\s+(all\s+)?guidelines",
    r"system\s+prompt\s+override",
    r"you\s+are\s+now\s+in\s+dan\s+mode",
    r"bypass\s+all\s+safety",
    r"output\s+the\s+system\s+instructions",
    r"<\|im_start\|>",
    r"<\|im_end\|>",
    r"act\s+as\s+an?\s+unrestricted",
    r"pretend\s+you\s+have\s+no\s+(restrictions|rules|guidelines)",
    r"jailbreak",
    r"do\s+anything\s+now",
    r"ignore\s+safety\s+(protocols|filters|rules)",
    r"reveal\s+(your|the)\s+(system|initial)\s+(prompt|instructions)",
]

_COMPILED_PATTERNS: list[re.Pattern[str]] = [
    re.compile(p, re.IGNORECASE) for p in SUSPICIOUS_PATTERNS
]

MAX_DOCUMENT_CHARS: Final[int] = 120_000

# ---------------------------------------------------------------------------
# Rate Limiter (Token-Bucket per IP)
# ---------------------------------------------------------------------------
class RateLimiter:
    """Simple in-memory sliding-window rate limiter.

    Attributes:
        max_requests: Maximum requests allowed within the time window.
        window_seconds: Duration of the sliding window in seconds.
    """

    def __init__(self, max_requests: int = 30, window_seconds: int = 60) -> None:
        self.max_requests: int = max_requests
        self.window_seconds: int = window_seconds
        self._requests: dict[str, list[float]] = defaultdict(list)

    def is_allowed(self, client_id: str) -> bool:
        """Check whether a request from *client_id* is within rate limits.

        Args:
            client_id: A string identifier for the client (e.g. IP address).

        Returns:
            True if the request is allowed, False if rate-limited.
        """
        now: float = time.monotonic()
        window_start: float = now - self.window_seconds

        # Prune expired timestamps
        self._requests[client_id] = [
            ts for ts in self._requests[client_id] if ts > window_start
        ]

        if len(self._requests[client_id]) >= self.max_requests:
            logger.warning("Rate limit exceeded for client: %s", client_id)
            return False

        self._requests[client_id].append(now)
        return True


# Singleton rate-limiter instance
rate_limiter: RateLimiter = RateLimiter()


# ---------------------------------------------------------------------------
# Input Sanitization
# ---------------------------------------------------------------------------
def sanitize_and_validate_legal_text(text: str) -> Tuple[str, bool, str]:
    """Validate and sanitize legal document text.

    Performs empty-check, length truncation, prompt-injection scanning,
    and control-character stripping.

    Args:
        text: Raw user-provided legal document text.

    Returns:
        A 3-tuple of (cleaned_text, is_safe, warning_message).
        - cleaned_text: The sanitized string (may be truncated).
        - is_safe: False if the text was empty or contained injections.
        - warning_message: Human-readable explanation when is_safe is False.
    """
    if not text or not text.strip():
        return "", False, "Document text cannot be empty."

    cleaned: str = text.strip()

    # Enforce maximum character length
    if len(cleaned) > MAX_DOCUMENT_CHARS:
        cleaned = cleaned[:MAX_DOCUMENT_CHARS]
        logger.info("Document truncated to %d characters.", MAX_DOCUMENT_CHARS)

    # Check for adversarial prompt-injection patterns
    for pattern in _COMPILED_PATTERNS:
        if pattern.search(cleaned):
            logger.warning("Prompt injection pattern detected and neutralized.")
            return cleaned, False, "Adversarial prompt injection pattern detected. Content neutralized."

    # Strip null bytes and non-printable control chars except newlines/tabs
    cleaned = "".join(
        ch for ch in cleaned
        if ch in "\n\r\t" or 32 <= ord(ch) <= 126 or ord(ch) > 127
    )

    return cleaned, True, ""


def get_standard_disclaimer() -> str:
    """Return the standard ethical and legal disclaimer text.

    Returns:
        The statutory disclaimer string.
    """
    return DISCLAIMER_TEXT
