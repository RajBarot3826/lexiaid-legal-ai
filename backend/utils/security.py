import re
from typing import Tuple

DISCLAIMER_TEXT = (
    "STATUTORY LEGAL NOTICE & ETHICAL DISCLAIMER: LexiAid is an artificial intelligence "
    "informational tool designed to help users read, understand, and organize legal documents. "
    "LexiAid does not provide formal legal advice, does not practice law, and does not create an "
    "attorney-client relationship. For binding legal representation or specific legal actions, "
    "always consult a licensed attorney or legal advocate in your jurisdiction."
)

# Common prompt injection signatures to protect LLM integrity
SUSPICIOUS_PATTERNS = [
    r"ignore\s+(all\s+)?(previous|prior)\s+instructions",
    r"disregard\s+(all\s+)?guidelines",
    r"system\s+prompt\s+override",
    r"you\s+are\s+now\s+in\s+dan\s+mode",
    r"bypass\s+all\s+safety",
    r"output\s+the\s+system\s+instructions",
    r"<\|im_start\|>",
    r"<\|im_end\|>",
]

MAX_DOCUMENT_CHARS = 120_000  # Approx 25,000 words / 50 pages

def sanitize_and_validate_legal_text(text: str) -> Tuple[str, bool, str]:
    """
    Validates and sanitizes legal document text.
    Returns: (cleaned_text, is_safe, warning_message)
    """
    if not text or not text.strip():
        return "", False, "Document text cannot be empty."

    cleaned = text.strip()

    # Enforce maximum character length
    if len(cleaned) > MAX_DOCUMENT_CHARS:
        cleaned = cleaned[:MAX_DOCUMENT_CHARS]

    # Check for adversarial prompt injection patterns
    for pattern in SUSPICIOUS_PATTERNS:
        if re.search(pattern, cleaned, re.IGNORECASE):
            return cleaned, False, "Adversarial prompt injection pattern detected. Content neutralized."

    # Strip null bytes and non-printable control chars except newlines and tabs
    cleaned = "".join(ch for ch in cleaned if ch in "\n\r\t" or 32 <= ord(ch) <= 126 or ord(ch) > 127)

    return cleaned, True, ""

def get_standard_disclaimer() -> str:
    return DISCLAIMER_TEXT
