"""Legal document analysis service.

Provides AI-powered and deterministic legal document analysis using
Google Gemini structured outputs with automatic fallback to the
offline mock engine when no API key is configured.

The analysis produces:
    - Clause-by-clause plain-English explanations
    - A 0-100 Legal Risk Index score
    - Identified red flags with severity ratings
    - Actionable due diligence checklists
    - Attorney consultation briefing packs
"""

import json
import logging

from backend.config import DEFAULT_MODEL, GEMINI_API_KEY, HAS_GEMINI_KEY
from backend.models.schemas import AnalyzeResponse
from backend.utils.security import get_standard_disclaimer
from backend.services.mock_engine import get_mock_analysis

# Configure module-level logger
logger: logging.Logger = logging.getLogger("lexiaid.analyzer")

# System prompt for Gemini structured output
ANALYSIS_SYSTEM_PROMPT: str = """You are LexiAid, an elite Legal Document Intelligence and Access AI assistant.
Your mission is to make legal contracts, leases, and agreements accessible, transparent, and actionable for non-lawyers.

Given the legal document, output a valid JSON object matching this exact structure:
{
  "document_title": "Descriptive Document Title",
  "document_type": "Category (e.g. Freelance Agreement, Residential Lease, NDA)",
  "overall_risk_score": 0-100,
  "risk_verdict": "Favorable" OR "Moderate Risk" OR "High Risk / Predatory",
  "executive_summary": "Concise 3-sentence summary.",
  "clauses": [{"clause_number": "", "original_title": "", "original_snippet": "", "plain_english": "", "risk_level": "Safe|Warning|Critical", "implication": ""}],
  "risks": [{"id": "", "category": "", "severity": "Critical|Warning|Low", "clause_title": "", "issue": "", "recommendation": "", "suggested_revision": ""}],
  "action_checklist": [{"id": "", "task": "", "category": "Before Signing|Post Signing|Ongoing", "trigger_or_deadline": "", "is_crucial": true}],
  "lawyer_prep": {"document_summary": "", "top_red_flags": [], "questions_to_ask": [], "negotiation_targets": [], "financial_exposure_note": ""}
}

Be thorough, objective, and highlight legal imbalances."""


def analyze_legal_document(
    text: str,
    reading_level: str = "Plain English",
    force_mock: bool = False,
) -> AnalyzeResponse:
    """Analyze a legal document and produce a structured risk assessment.

    Attempts live Gemini API analysis first, falling back to the
    deterministic mock engine on failure or when forced.

    Args:
        text: Sanitized legal document text.
        reading_level: Target reading level (Plain English, Executive, ELI5).
        force_mock: If True, bypass Gemini and use the mock engine.

    Returns:
        An AnalyzeResponse with risk scores, clause breakdowns, and advice.
    """
    # Use deterministic engine if no API key or forced mock mode
    if force_mock or not HAS_GEMINI_KEY:
        return get_mock_analysis(text, reading_level)

    try:
        from google import genai

        client = genai.Client(api_key=GEMINI_API_KEY)
        prompt: str = (
            f"Reading Level Target: {reading_level}\n\n"
            f'Document Text:\n"""\n{text}\n"""'
        )

        response = client.models.generate_content(
            model=DEFAULT_MODEL,
            contents=prompt,
            config={
                "system_instruction": ANALYSIS_SYSTEM_PROMPT,
                "response_mime_type": "application/json",
            },
        )

        data: dict = json.loads(response.text)
        data["disclaimer"] = get_standard_disclaimer()
        return AnalyzeResponse(**data)
    except Exception as exc:
        logger.warning(
            "Gemini API analysis failed: %s. Falling back to mock engine.", exc
        )
        return get_mock_analysis(text, reading_level)
