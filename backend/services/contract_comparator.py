"""Contract comparison service.

Compares two legal documents to identify divergences, additions,
omissions, and relative party favorability using Google Gemini AI
with automatic fallback to the deterministic mock engine.
"""

import json
import logging

from backend.config import DEFAULT_MODEL, GEMINI_API_KEY, HAS_GEMINI_KEY
from backend.models.schemas import CompareResponse
from backend.utils.security import get_standard_disclaimer
from backend.services.mock_engine import get_mock_comparison

# Configure module-level logger
logger: logging.Logger = logging.getLogger("lexiaid.comparator")

# System prompt for Gemini structured comparison output
COMPARISON_SYSTEM_PROMPT: str = """You are LexiAid's Contract Comparison Engine.
Compare two legal documents and identify key divergences, additions, omissions, and party favorability.

Output a valid JSON object matching this structure:
{
  "comparison_title": "",
  "executive_summary": "",
  "favorability_score_a": 0-100,
  "favorability_score_b": 0-100,
  "comparisons": [{"topic": "", "contract_a_terms": "", "contract_b_terms": "", "divergence_level": "Minor|Significant|Major Conflict", "favors": "Contract A|Contract B|Neutral", "analysis": ""}],
  "critical_differences": [],
  "negotiation_advice": ""
}"""


def compare_legal_documents(
    contract_a: str,
    contract_b: str,
    name_a: str = "Contract A",
    name_b: str = "Contract B",
    force_mock: bool = False,
) -> CompareResponse:
    """Compare two legal documents and produce a structured divergence report.

    Args:
        contract_a: Sanitized text of the first contract.
        contract_b: Sanitized text of the second contract.
        name_a: Display name for contract A.
        name_b: Display name for contract B.
        force_mock: If True, bypass Gemini and use the mock engine.

    Returns:
        A CompareResponse with favorability scores and clause comparisons.
    """
    # Use deterministic engine if no API key or forced mock mode
    if force_mock or not HAS_GEMINI_KEY:
        return get_mock_comparison(contract_a, contract_b, name_a, name_b)

    try:
        from google import genai

        client = genai.Client(api_key=GEMINI_API_KEY)
        prompt: str = (
            f"Compare these two contracts:\n\n"
            f"=== {name_a} ===\n{contract_a}\n\n"
            f"=== {name_b} ===\n{contract_b}\n"
        )

        response = client.models.generate_content(
            model=DEFAULT_MODEL,
            contents=prompt,
            config={
                "system_instruction": COMPARISON_SYSTEM_PROMPT,
                "response_mime_type": "application/json",
            },
        )

        data: dict = json.loads(response.text)
        data["disclaimer"] = get_standard_disclaimer()
        return CompareResponse(**data)
    except Exception as exc:
        logger.warning(
            "Gemini comparison failed: %s. Falling back to mock engine.", exc
        )
        return get_mock_comparison(contract_a, contract_b, name_a, name_b)
