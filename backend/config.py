"""Application configuration module for LexiAid.

Loads environment variables for API keys, model selection, and server
configuration. Provides centralized constants used throughout the application
to avoid magic strings and ensure consistency.

Environment Variables:
    GEMINI_API_KEY: Google Gemini API key for live AI analysis.
    GOOGLE_API_KEY: Alternative API key environment variable.
    GEMINI_MODEL: Gemini model identifier (default: gemini-2.5-flash).
    PORT: Server port (default: 8000).
    HOST: Server host (default: 0.0.0.0).
"""

import logging
import os
from typing import Final

from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()

# Configure module-level logger
logger: logging.Logger = logging.getLogger("lexiaid.config")

# ---------------------------------------------------------------------------
# API & Model Configuration
# ---------------------------------------------------------------------------
GEMINI_API_KEY: Final[str] = (
    os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY") or ""
)
DEFAULT_MODEL: Final[str] = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

# ---------------------------------------------------------------------------
# Server Configuration
# ---------------------------------------------------------------------------
APP_PORT: Final[int] = int(os.getenv("PORT", "8000"))
APP_HOST: Final[str] = os.getenv("HOST", "0.0.0.0")

# ---------------------------------------------------------------------------
# Feature Flags
# ---------------------------------------------------------------------------
HAS_GEMINI_KEY: Final[bool] = bool(GEMINI_API_KEY.strip())

# ---------------------------------------------------------------------------
# Security Constants
# ---------------------------------------------------------------------------
MAX_DOCUMENT_CHARS: Final[int] = 120_000
MAX_REQUEST_BODY_BYTES: Final[int] = 1_048_576  # 1 MiB

# ---------------------------------------------------------------------------
# CORS Configuration
# ---------------------------------------------------------------------------
# Allow all origins for hackathon evaluation compatibility.
# In production, restrict to specific domains.
ALLOWED_ORIGINS: Final[list[str]] = ["*"]

# Log startup configuration
if HAS_GEMINI_KEY:
    logger.info(
        "Gemini API key detected - live AI mode enabled (model: %s).",
        DEFAULT_MODEL,
    )
else:
    logger.info("No Gemini API key - deterministic offline engine active.")
