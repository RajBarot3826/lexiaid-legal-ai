from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class AnalyzeRequest(BaseModel):
    text: str = Field(..., min_length=20, description="Raw legal document text")
    doc_type: Optional[str] = Field("General Agreement", description="Optional hint for document category")
    reading_level: Optional[str] = Field("Plain English", description="Plain English, Executive, or ELI5")
    force_mock: Optional[bool] = Field(False, description="Force deterministic mock mode for testing")

class ClauseExplanation(BaseModel):
    clause_number: str
    original_title: str
    original_snippet: str
    plain_english: str
    risk_level: str = Field(..., description="Safe, Warning, Critical")
    implication: str

class RiskItem(BaseModel):
    id: str
    category: str = Field(..., description="Liability, Termination, IP Rights, Non-Compete, Jurisdiction, Financial")
    severity: str = Field(..., description="Critical, Warning, Low")
    clause_title: str
    issue: str
    recommendation: str
    suggested_revision: Optional[str] = None

class ChecklistItem(BaseModel):
    id: str
    task: str
    category: str = Field(..., description="Before Signing, Post Signing, Ongoing")
    trigger_or_deadline: str
    is_crucial: bool = True

class LawyerPrep(BaseModel):
    document_summary: str
    top_red_flags: List[str]
    questions_to_ask: List[str]
    negotiation_targets: List[str]
    financial_exposure_note: str

class AnalyzeResponse(BaseModel):
    document_title: str
    document_type: str
    overall_risk_score: int = Field(..., ge=0, le=100, description="0 (Zero Risk) to 100 (Severe/Predatory)")
    risk_verdict: str = Field(..., description="Favorable, Moderate Risk, High Risk / Predatory")
    executive_summary: str
    clauses: List[ClauseExplanation]
    risks: List[RiskItem]
    action_checklist: List[ChecklistItem]
    lawyer_prep: LawyerPrep
    disclaimer: str

class CompareRequest(BaseModel):
    contract_a_text: str = Field(..., min_length=20)
    contract_b_text: str = Field(..., min_length=20)
    name_a: Optional[str] = "Standard Contract (Version A)"
    name_b: Optional[str] = "Revised Contract (Version B)"
    force_mock: Optional[bool] = False

class ClauseComparison(BaseModel):
    topic: str
    contract_a_terms: str
    contract_b_terms: str
    divergence_level: str = Field(..., description="Minor, Significant, Major Conflict")
    favors: str = Field(..., description="Contract A, Contract B, Neutral")
    analysis: str

class CompareResponse(BaseModel):
    comparison_title: str
    executive_summary: str
    favorability_score_a: int = Field(..., ge=0, le=100)
    favorability_score_b: int = Field(..., ge=0, le=100)
    comparisons: List[ClauseComparison]
    critical_differences: List[str]
    negotiation_advice: str
    disclaimer: str

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    document_text: str = Field(..., min_length=20)
    query: str = Field(..., min_length=3)
    history: Optional[List[ChatMessage]] = []
    force_mock: Optional[bool] = False

class ChatResponse(BaseModel):
    answer: str
    citations: List[str]
    risk_note: Optional[str] = None
    follow_up_suggestions: List[str]
    disclaimer: str

class SimplifyRequest(BaseModel):
    clause_text: str = Field(..., min_length=10)
    reading_level: Optional[str] = "Plain English"

class SimplifyResponse(BaseModel):
    original: str
    simplified: str
    reading_level: str
    key_takeaway: str
    risk_verdict: str
