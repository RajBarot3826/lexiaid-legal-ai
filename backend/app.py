import os
from pathlib import Path
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse

from .models.schemas import (
    AnalyzeRequest, AnalyzeResponse,
    CompareRequest, CompareResponse,
    ChatRequest, ChatResponse,
    SimplifyRequest, SimplifyResponse
)
from .services.legal_analyzer import analyze_legal_document
from .services.contract_comparator import compare_legal_documents
from .services.legal_chat import answer_legal_query
from .services.mock_engine import get_mock_simplification
from .utils.security import sanitize_and_validate_legal_text, get_standard_disclaimer
from .config import HAS_GEMINI_KEY, DEFAULT_MODEL

app = FastAPI(
    title="LexiAid - AI for Legal Assistance & Access",
    description="Democratizing legal comprehension with Plain-English simplification, Risk Auditing, and Contract Intelligence.",
    version="1.0.0"
)

# Enable CORS for local testing and cross-origin clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SAMPLE_DIR = Path(__file__).resolve().parent.parent / "sample_contracts"

@app.get("/api/health")
def health_check():
    return {
        "status": "online",
        "service": "LexiAid Legal Intelligence API",
        "version": "1.0.0",
        "gemini_active": HAS_GEMINI_KEY,
        "default_model": DEFAULT_MODEL,
        "mode": "Live Gemini" if HAS_GEMINI_KEY else "Deterministic Offline Engine"
    }

@app.get("/api/samples")
def list_sample_contracts():
    """Returns pre-loaded realistic sample contracts for 1-click evaluation."""
    samples = []
    if SAMPLE_DIR.exists():
        for file in SAMPLE_DIR.glob("*.txt"):
            samples.append({
                "id": file.stem,
                "title": file.stem.replace("_", " ").title(),
                "content": file.read_text(encoding="utf-8")
            })
    return {"samples": samples}

@app.post("/api/analyze", response_model=AnalyzeResponse)
def analyze_document(request: AnalyzeRequest):
    cleaned, is_safe, warning = sanitize_and_validate_legal_text(request.text)
    if not cleaned:
        raise HTTPException(status_code=400, detail="Invalid or empty document text.")
    
    response = analyze_legal_document(
        text=cleaned,
        reading_level=request.reading_level or "Plain English",
        force_mock=request.force_mock or not is_safe
    )
    return response

@app.post("/api/compare", response_model=CompareResponse)
def compare_contracts(request: CompareRequest):
    cleaned_a, _, _ = sanitize_and_validate_legal_text(request.contract_a_text)
    cleaned_b, _, _ = sanitize_and_validate_legal_text(request.contract_b_text)
    
    if not cleaned_a or not cleaned_b:
        raise HTTPException(status_code=400, detail="Both contracts must contain valid text.")
    
    response = compare_legal_documents(
        contract_a=cleaned_a,
        contract_b=cleaned_b,
        name_a=request.name_a or "Contract A",
        name_b=request.name_b or "Contract B",
        force_mock=request.force_mock
    )
    return response

@app.post("/api/chat", response_model=ChatResponse)
def chat_with_document(request: ChatRequest):
    cleaned_doc, _, _ = sanitize_and_validate_legal_text(request.document_text)
    if not cleaned_doc:
        raise HTTPException(status_code=400, detail="Valid document text is required for Q&A.")
    
    response = answer_legal_query(
        query=request.query,
        document_text=cleaned_doc,
        history=request.history,
        force_mock=request.force_mock
    )
    return response

@app.post("/api/simplify", response_model=SimplifyResponse)
def simplify_clause(request: SimplifyRequest):
    return get_mock_simplification(request.clause_text, request.reading_level or "Plain English")

# Mount static frontend files if directory exists
FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"
if FRONTEND_DIR.exists():
    app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")
