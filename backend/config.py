import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY") or ""
DEFAULT_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
APP_PORT = int(os.getenv("PORT", "8000"))
APP_HOST = os.getenv("HOST", "0.0.0.0")

# Whether live Gemini is available
HAS_GEMINI_KEY = bool(GEMINI_API_KEY.strip())
