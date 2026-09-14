import json
import logging
from ..config import GEMINI_API_KEY, DEFAULT_MODEL, HAS_GEMINI_KEY
from ..models.schemas import AnalyzeResponse, ClauseExplanation, RiskItem, ChecklistItem, LawyerPrep
from ..utils.security import get_standard_disclaimer
from .mock_engine import get_mock_analysis

logger = logging.getLogger("lexiaid.analyzer")

ANALYSIS_SYSTEM_PROMPT = """You are LexiAid, an elite Legal Document Intelligence and Access AI assistant.
Your mission is to make legal contracts, leases, and agreements accessible, transparent, and actionable for non-lawyers.

Given the legal document, output a valid JSON object matching this exact structure:
{
  "document_title": "Descriptive Document Title",
  "document_type": "Category (e.g. Freelance Agreement, Residential Lease, NDA)",
  "overall_risk_score": 0-100 (0 = completely safe/favorable, 100 = predatory/catastrophic risk),
  "risk_verdict": "Favorable" OR "Moderate Risk" OR "High Risk / Predatory",
  "executive_summary": "Concise 3-sentence summary in plain English explaining what the contract is and the biggest takeaway.",
  "clauses": [
    {
      "clause_number": "Clause 1",
      "original_title": "Clause Name",
      "original_snippet": "Key verbatim text excerpt...",
      "plain_english": "What this actually means for the user in simple everyday words.",
      "risk_level": "Safe" OR "Warning" OR "Critical",
      "implication": "Real-world consequence of this clause."
    }
  ],
  "risks": [
    {
      "id": "RISK-01",
      "category": "Liability" OR "Termination" OR "IP Rights" OR "Non-Compete" OR "Jurisdiction" OR "Financial",
      "severity": "Critical" OR "Warning" OR "Low",
      "clause_title": "Clause reference",
      "issue": "Specific explanation of the danger/unfavorable term",
      "recommendation": "What the user should do or negotiate",
      "suggested_revision": "Exact counter-proposal wording"
    }
  ],
  "action_checklist": [
    {
      "id": "CHK-01",
      "task": "Concrete task description",
      "category": "Before Signing" OR "Post Signing" OR "Ongoing",
      "trigger_or_deadline": "When this must be done",
      "is_crucial": true or false
    }
  ],
  "lawyer_prep": {
    "document_summary": "1-line summary for counsel",
    "top_red_flags": ["List of biggest legal vulnerabilities"],
    "questions_to_ask": ["3-5 targeted legal questions for an attorney consultation"],
    "negotiation_targets": ["Key clauses to push back on"],
    "financial_exposure_note": "Summary of total monetary and liability exposure"
  }
}

Be thorough, objective, and highlight legal imbalances like uncapped liabilities, one-sided termination, overbroad non-competes, and jurisdiction traps.
"""

def analyze_legal_document(text: str, reading_level: str = "Plain English", force_mock: bool = False) -> AnalyzeResponse:
    if force_mock or not HAS_GEMINI_KEY:
        return get_mock_analysis(text, reading_level)

    try:
        from google import genai
        client = genai.Client(api_key=GEMINI_API_KEY)
        
        prompt = f"Reading Level Target: {reading_level}\n\nDocument Text:\n\"\"\"\n{text}\n\"\"\""
        
        response = client.models.generate_content(
            model=DEFAULT_MODEL,
            contents=prompt,
            config={
                "system_instruction": ANALYSIS_SYSTEM_PROMPT,
                "response_mime_type": "application/json",
            }
        )

        data = json.loads(response.text)
        data["disclaimer"] = get_standard_disclaimer()
        return AnalyzeResponse(**data)
    except Exception as e:
        logger.warning(f"Live Gemini API call failed or timed out: {e}. Falling back to deterministic mock engine.")
        return get_mock_analysis(text, reading_level)
