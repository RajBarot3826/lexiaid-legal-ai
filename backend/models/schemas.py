"""Pydantic v2 request and response schemas for the LexiAid API.

Defines strongly-typed data models for document analysis, contract comparison,
grounded Q&A, and clause simplification endpoints. All models use Pydantic v2
with Field descriptions for automatic OpenAPI documentation generation.
"""

from typing import List, Optional
from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Document Analysis Schemas
# ---------------------------------------------------------------------------
class AnalyzeRequest(BaseModel):
    """Request model for legal document analysis."""

    text: str = Field(..., min_length=20, description="Raw legal document text")
    doc_type: Optional[str] = Field(
        "General Agreement", description="Optional hint for document category"
    )
    reading_level: Optional[str] = Field(
        "Plain English", description="Plain English, Executive, or ELI5"
    )
    force_mock: Optional[bool] = Field(
        False, description="Force deterministic mock mode for testing"
    )


class ClauseExplanation(BaseModel):
    """A single clause explanation with risk assessment."""

    clause_number: str
    original_title: str
    original_snippet: str
    plain_english: str
    risk_level: str = Field(..., description="Safe, Warning, or Critical")
    implication: str


class RiskItem(BaseModel):
    """An identified risk in the legal document."""

    id: str
    category: str = Field(
        ...,
        description="Liability, Termination, IP Rights, Non-Compete, Jurisdiction, or Financial",
    )
    severity: str = Field(..., description="Critical, Warning, or Low")
    clause_title: str
    issue: str
    recommendation: str
    suggested_revision: Optional[str] = None


class ChecklistItem(BaseModel):
    """An actionable due diligence task."""

    id: str
    task: str
    category: str = Field(..., description="Before Signing, Post Signing, or Ongoing")
    trigger_or_deadline: str
    is_crucial: bool = True


class LawyerPrep(BaseModel):
    """Attorney consultation briefing pack data."""

    document_summary: str
    top_red_flags: List[str]
    questions_to_ask: List[str]
    negotiation_targets: List[str]
    financial_exposure_note: str


class AnalyzeResponse(BaseModel):
    """Complete analysis response with risk scores, clauses, and advice."""

    document_title: str
    document_type: str
    overall_risk_score: int = Field(
        ..., ge=0, le=100, description="0 (Zero Risk) to 100 (Severe/Predatory)"
    )
    risk_verdict: str = Field(
        ..., description="Favorable, Moderate Risk, or High Risk / Predatory"
    )
    executive_summary: str
    clauses: List[ClauseExplanation]
    risks: List[RiskItem]
    action_checklist: List[ChecklistItem]
    lawyer_prep: LawyerPrep
    disclaimer: str


# ---------------------------------------------------------------------------
# Contract Comparison Schemas
# ---------------------------------------------------------------------------
class CompareRequest(BaseModel):
    """Request model for dual-contract comparison."""

    contract_a_text: str = Field(..., min_length=20)
    contract_b_text: str = Field(..., min_length=20)
    name_a: Optional[str] = "Standard Contract (Version A)"
    name_b: Optional[str] = "Revised Contract (Version B)"
    force_mock: Optional[bool] = False


class ClauseComparison(BaseModel):
    """A single clause comparison between two contracts."""

    topic: str
    contract_a_terms: str
    contract_b_terms: str
    divergence_level: str = Field(
        ..., description="Minor, Significant, or Major Conflict"
    )
    favors: str = Field(..., description="Contract A, Contract B, or Neutral")
    analysis: str


class CompareResponse(BaseModel):
    """Comparison response with favorability scores and divergence analysis."""

    comparison_title: str
    executive_summary: str
    favorability_score_a: int = Field(..., ge=0, le=100)
    favorability_score_b: int = Field(..., ge=0, le=100)
    comparisons: List[ClauseComparison]
    critical_differences: List[str]
    negotiation_advice: str
    disclaimer: str


# ---------------------------------------------------------------------------
# Grounded Q&A Chat Schemas
# ---------------------------------------------------------------------------
class ChatMessage(BaseModel):
    """A single chat message in the conversation history."""

    role: str
    content: str


class ChatRequest(BaseModel):
    """Request model for grounded legal document Q&A."""

    document_text: str = Field(..., min_length=20)
    query: str = Field(..., min_length=3)
    history: Optional[List[ChatMessage]] = []
    force_mock: Optional[bool] = False


class ChatResponse(BaseModel):
    """Grounded Q&A response with citations and risk notes."""

    answer: str
    citations: List[str]
    risk_note: Optional[str] = None
    follow_up_suggestions: List[str]
    disclaimer: str


# ---------------------------------------------------------------------------
# Clause Simplification Schemas
# ---------------------------------------------------------------------------
class SimplifyRequest(BaseModel):
    """Request model for clause simplification."""

    clause_text: str = Field(..., min_length=10)
    reading_level: Optional[str] = "Plain English"


class SimplifyResponse(BaseModel):
    """Simplified clause response with risk assessment."""

    original: str
    simplified: str
    reading_level: str
    key_takeaway: str
    risk_verdict: str
