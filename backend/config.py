"""Application configuration module for LexiAid.

Loads environment variables for API keys, model selection, and server
configuration. Provides centralized constants used throughout the application.
"""

import logging
import os
from typing import Final

from dotenv import load_dotenv

load_dotenv()

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
RATE_LIMIT_REQUESTS: Final[int] = 30
RATE_LIMIT_WINDOW_SECONDS: Final[int] = 60

# ---------------------------------------------------------------------------
# Allowed Origins (CORS)
# ---------------------------------------------------------------------------
ALLOWED_ORIGINS: Final[list[str]] = [
    "https://rajbarot3826.github.io",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://localhost:3000",
]

if HAS_GEMINI_KEY:
    logger.info("Gemini API key detected – live AI mode enabled (model: %s).", DEFAULT_MODEL)
else:
    logger.info("No Gemini API key – deterministic offline engine active.")
