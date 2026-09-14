"""LexiAid FastAPI application module.

Provides REST API endpoints for legal document analysis, contract comparison,
grounded Q&A, clause simplification, and sample contract retrieval.

Features:
    - Asynchronous request handlers for high concurrency.
    - LRU-cached sample contract loading for efficient I/O.
    - Hash-based analysis result caching to avoid redundant processing.
    - Response timing headers for performance monitoring.
    - Security headers middleware for defense-in-depth.
    - CORS middleware for cross-origin frontend access.
    - OWASP-style input sanitization on all endpoints.
"""

import hashlib
import logging
import time
from functools import lru_cache
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.config import ALLOWED_ORIGINS, DEFAULT_MODEL, HAS_GEMINI_KEY
from backend.models.schemas import (
    AnalyzeRequest,
    AnalyzeResponse,
    ChatRequest,
    ChatResponse,
    CompareRequest,
    CompareResponse,
    SimplifyRequest,
    SimplifyResponse,
)
from backend.services.contract_comparator import compare_legal_documents
from backend.services.legal_analyzer import analyze_legal_document
from backend.services.legal_chat import answer_legal_query
from backend.services.mock_engine import get_mock_simplification
from backend.utils.security import (
    get_standard_disclaimer,
    sanitize_and_validate_legal_text,
)

# Configure module-level logger
logger: logging.Logger = logging.getLogger("lexiaid.api")

# Configure root logger for structured output
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(name)-22s | %(levelname)-7s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# ---------------------------------------------------------------------------
# Application Instance
# ---------------------------------------------------------------------------
app: FastAPI = FastAPI(
    title="LexiAid - AI for Legal Assistance & Access",
    description=(
        "Democratizing legal comprehension with Plain-English simplification, "
        "Risk Auditing, and Contract Intelligence. Built for PromptWars: Virtual."
    ),
    version="1.0.0",
)

# ---------------------------------------------------------------------------
# CORS Middleware
# ---------------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)


# ---------------------------------------------------------------------------
# Middleware: Request Timing & Security Headers
# ---------------------------------------------------------------------------
@app.middleware("http")
async def timing_and_security_headers_middleware(
    request: Request, call_next: Any
) -> Response:
    """Add processing-time measurement and security headers to every response.

    Measures wall-clock time from request receipt to response send and
    injects the result as an X-Processing-Time-Ms header. Also adds
    standard security hardening headers.
    """
    start_time: float = time.monotonic()

    response: Response = await call_next(request)

    # Performance timing header
    elapsed_ms: float = (time.monotonic() - start_time) * 1000
    response.headers["X-Processing-Time-Ms"] = f"{elapsed_ms:.1f}"

    # Security hardening headers
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

    return response


# ---------------------------------------------------------------------------
# Lazy-Loaded Sample Contracts (on-demand I/O with caching)
# ---------------------------------------------------------------------------
SAMPLE_DIR: Path = Path(__file__).resolve().parent.parent / "sample_contracts"


@lru_cache(maxsize=1)
def _load_samples() -> list[dict[str, str]]:
    """Load sample contracts from disk lazily and cache the result.

    Uses functools.lru_cache to ensure disk I/O happens only once,
    regardless of how many times the endpoint is called.

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
    """Generate a deterministic cache key from document text and reading level.

    Uses SHA-256 hashing to create a fixed-length key that uniquely
    identifies the combination of document content and reading level.

    Args:
        text: The sanitized document text.
        reading_level: The target reading level.

    Returns:
        A hex-encoded SHA-256 hash string.
    """
    return hashlib.sha256(f"{reading_level}::{text}".encode("utf-8")).hexdigest()


# ---------------------------------------------------------------------------
# API Endpoints
# ---------------------------------------------------------------------------
@app.get("/api/health")
async def health_check() -> dict[str, Any]:
    """Return service health status and configuration summary.

    Returns:
        A dictionary with service status, version, AI mode, and model info.
    """
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
    """Return pre-loaded realistic sample contracts for 1-click evaluation.

    Returns:
        A dictionary containing a 'samples' list with contract data.
    """
    return {"samples": _load_samples()}


@app.post("/api/analyze", response_model=AnalyzeResponse)
async def analyze_document(request: AnalyzeRequest) -> AnalyzeResponse:
    """Analyze a legal document for risks, clause breakdown, and actionable advice.

    Performs OWASP input sanitization, checks the analysis cache for
    duplicate requests, then delegates to the Gemini AI or deterministic
    mock engine for comprehensive legal document analysis.

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

    # Return cached result if available (efficiency optimization)
    if key in _analysis_cache and not request.force_mock:
        logger.info("Cache hit for analysis request.")
        return _analysis_cache[key]

    # Perform analysis via Gemini AI or deterministic fallback
    response: AnalyzeResponse = analyze_legal_document(
        text=cleaned,
        reading_level=reading_level,
        force_mock=request.force_mock or not is_safe,
    )

    # Cache the result for future identical requests
    _analysis_cache[key] = response
    return response


@app.post("/api/compare", response_model=CompareResponse)
async def compare_contracts(request: CompareRequest) -> CompareResponse:
    """Compare two legal contracts and surface divergences and favorability.

    Sanitizes both contract texts, then delegates to the comparison engine
    to identify clause-level differences and compute favorability scores.

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

    All answers are strictly bounded to the document text with verbatim
    citations to prevent hallucination and ensure factual accuracy.

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

    Translates complex legalese into accessible language at the
    specified reading level with risk assessment.

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
