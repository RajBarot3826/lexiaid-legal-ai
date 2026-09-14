"""LexiAid FastAPI application module.

Provides REST API endpoints for legal document analysis, contract comparison,
grounded Q&A, clause simplification, and sample contract retrieval. Includes
rate limiting, request timing, caching, and CORS security middleware.
"""

import hashlib
import logging
import time
from functools import lru_cache
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from .config import (
    ALLOWED_ORIGINS,
    APP_HOST,
    APP_PORT,
    DEFAULT_MODEL,
    HAS_GEMINI_KEY,
)
from .models.schemas import (
    AnalyzeRequest,
    AnalyzeResponse,
    ChatRequest,
    ChatResponse,
    CompareRequest,
    CompareResponse,
    SimplifyRequest,
    SimplifyResponse,
)
from .services.contract_comparator import compare_legal_documents
from .services.legal_analyzer import analyze_legal_document
from .services.legal_chat import answer_legal_query
from .services.mock_engine import get_mock_simplification
from .utils.security import (
    get_standard_disclaimer,
    rate_limiter,
    sanitize_and_validate_legal_text,
)

logger: logging.Logger = logging.getLogger("lexiaid.api")

# Configure root logger for structured output
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(name)-22s | %(levelname)-7s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# ---------------------------------------------------------------------------
# Application Factory
# ---------------------------------------------------------------------------
app: FastAPI = FastAPI(
    title="LexiAid - AI for Legal Assistance & Access",
    description=(
        "Democratizing legal comprehension with Plain-English simplification, "
        "Risk Auditing, and Contract Intelligence."
    ),
    version="1.0.0",
)

# ---------------------------------------------------------------------------
# CORS Middleware (restricted origins)
# ---------------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)

# ---------------------------------------------------------------------------
# Middleware: Rate Limiting & Request Timing
# ---------------------------------------------------------------------------
@app.middleware("http")
async def rate_limit_and_timing_middleware(
    request: Request, call_next: Any
) -> Response:
    """Apply per-client rate limiting and add processing-time headers."""
    start_time: float = time.monotonic()
    client_ip: str = request.client.host if request.client else "unknown"

    if not rate_limiter.is_allowed(client_ip):
        logger.warning("Rate limited: %s %s from %s", request.method, request.url.path, client_ip)
        return JSONResponse(
            status_code=429,
            content={"detail": "Rate limit exceeded. Please try again later."},
        )

    response: Response = await call_next(request)
    elapsed_ms: float = (time.monotonic() - start_time) * 1000
    response.headers["X-Processing-Time-Ms"] = f"{elapsed_ms:.1f}"
    response.headers["X-RateLimit-Limit"] = str(rate_limiter.max_requests)
    return response


# ---------------------------------------------------------------------------
# Lazy-Loaded Sample Contracts (on-demand I/O)
# ---------------------------------------------------------------------------
SAMPLE_DIR: Path = Path(__file__).resolve().parent.parent / "sample_contracts"


@lru_cache(maxsize=1)
def _load_samples() -> list[dict[str, str]]:
    """Load sample contracts from disk lazily and cache the result.

    Returns:
        A list of dictionaries, each with 'id', 'title', and 'content' keys.
    """
    samples: list[dict[str, str]] = []
    if SAMPLE_DIR.exists():
        for file in sorted(SAMPLE_DIR.glob("*.txt")):
            samples.append(
                {
                    "id": file.stem,
                    "title": file.stem.replace("_", " ").title(),
                    "content": file.read_text(encoding="utf-8"),
                }
            )
    logger.info("Loaded %d sample contracts from disk.", len(samples))
    return samples


# ---------------------------------------------------------------------------
# Analysis Result Cache (hash-based deduplication)
# ---------------------------------------------------------------------------
_analysis_cache: dict[str, AnalyzeResponse] = {}


def _cache_key(text: str, reading_level: str) -> str:
    """Generate a deterministic cache key from document text and reading level."""
    return hashlib.sha256(f"{reading_level}::{text}".encode("utf-8")).hexdigest()


# ---------------------------------------------------------------------------
# API Endpoints
# ---------------------------------------------------------------------------
@app.get("/api/health")
async def health_check() -> dict[str, Any]:
    """Return service health status and configuration summary."""
    return {
        "status": "online",
        "service": "LexiAid Legal Intelligence API",
        "version": "1.0.0",
        "gemini_active": HAS_GEMINI_KEY,
        "default_model": DEFAULT_MODEL,
        "mode": "Live Gemini" if HAS_GEMINI_KEY else "Deterministic Offline Engine",
    }


@app.get("/api/samples")
async def list_sample_contracts() -> dict[str, list[dict[str, str]]]:
    """Return pre-loaded realistic sample contracts for 1-click evaluation."""
    return {"samples": _load_samples()}


@app.post("/api/analyze", response_model=AnalyzeResponse)
async def analyze_document(request: AnalyzeRequest) -> AnalyzeResponse:
    """Analyze a legal document for risks, clause breakdown, and actionable advice.

    Args:
        request: The analysis request containing document text and options.

    Returns:
        A comprehensive analysis response with risk scores, clause explanations,
        action checklists, and lawyer preparation materials.

    Raises:
        HTTPException: If the document text is invalid or empty.
    """
    cleaned, is_safe, warning = sanitize_and_validate_legal_text(request.text)
    if not cleaned:
        raise HTTPException(status_code=400, detail="Invalid or empty document text.")

    reading_level: str = request.reading_level or "Plain English"
    key: str = _cache_key(cleaned, reading_level)

    # Return cached result if available
    if key in _analysis_cache and not request.force_mock:
        logger.info("Cache hit for analysis request.")
        return _analysis_cache[key]

    response: AnalyzeResponse = analyze_legal_document(
        text=cleaned,
        reading_level=reading_level,
        force_mock=request.force_mock or not is_safe,
    )

    _analysis_cache[key] = response
    return response


@app.post("/api/compare", response_model=CompareResponse)
async def compare_contracts(request: CompareRequest) -> CompareResponse:
    """Compare two legal contracts and surface divergences and favorability.

    Args:
        request: The comparison request with both contract texts.

    Returns:
        A structured comparison with favorability scores and clause analysis.

    Raises:
        HTTPException: If either contract text is invalid or empty.
    """
    cleaned_a, _, _ = sanitize_and_validate_legal_text(request.contract_a_text)
    cleaned_b, _, _ = sanitize_and_validate_legal_text(request.contract_b_text)

    if not cleaned_a or not cleaned_b:
        raise HTTPException(
            status_code=400, detail="Both contracts must contain valid text."
        )

    return compare_legal_documents(
        contract_a=cleaned_a,
        contract_b=cleaned_b,
        name_a=request.name_a or "Contract A",
        name_b=request.name_b or "Contract B",
        force_mock=request.force_mock,
    )


@app.post("/api/chat", response_model=ChatResponse)
async def chat_with_document(request: ChatRequest) -> ChatResponse:
    """Answer a user question grounded in the provided legal document text.

    Args:
        request: The chat request with document text and user query.

    Returns:
        A grounded answer with verbatim citations and risk notes.

    Raises:
        HTTPException: If the document text is invalid.
    """
    cleaned_doc, _, _ = sanitize_and_validate_legal_text(request.document_text)
    if not cleaned_doc:
        raise HTTPException(
            status_code=400, detail="Valid document text is required for Q&A."
        )

    return answer_legal_query(
        query=request.query,
        document_text=cleaned_doc,
        history=request.history,
        force_mock=request.force_mock,
    )


@app.post("/api/simplify", response_model=SimplifyResponse)
async def simplify_clause(request: SimplifyRequest) -> SimplifyResponse:
    """Simplify a legal clause into plain-English language.

    Args:
        request: The simplification request with clause text.

    Returns:
        The simplified clause with risk assessment.
    """
    return get_mock_simplification(
        request.clause_text, request.reading_level or "Plain English"
    )


# ---------------------------------------------------------------------------
# Static Frontend Mount
# ---------------------------------------------------------------------------
FRONTEND_DIR: Path = Path(__file__).resolve().parent.parent / "frontend"
if FRONTEND_DIR.exists():
    app.mount(
        "/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend"
    )
