import json
import logging
from ..config import GEMINI_API_KEY, DEFAULT_MODEL, HAS_GEMINI_KEY
from ..models.schemas import CompareResponse, ClauseComparison
from ..utils.security import get_standard_disclaimer
from .mock_engine import get_mock_comparison

logger = logging.getLogger("lexiaid.comparator")

COMPARISON_SYSTEM_PROMPT = """You are LexiAid's Contract Comparison Engine.
Compare two legal documents or contract drafts and identify key divergences, additions, omissions, and party favorability.

Output a valid JSON object matching this structure:
{
  "comparison_title": "Descriptive Comparison Title",
  "executive_summary": "High-level plain-English narrative comparing the two versions.",
  "favorability_score_a": 0-100 (Overall favorability score for Version A),
  "favorability_score_b": 0-100 (Overall favorability score for Version B),
  "comparisons": [
    {
      "topic": "Topic Name (e.g., Liability, Termination, Confidentiality)",
      "contract_a_terms": "Summary of Version A's terms",
      "contract_b_terms": "Summary of Version B's terms",
      "divergence_level": "Minor" OR "Significant" OR "Major Conflict",
      "favors": "Contract A" OR "Contract B" OR "Neutral",
      "analysis": "Specific explanation of which party benefits and why."
    }
  ],
  "critical_differences": [
    "Bulleted summary of the biggest traps or discrepancies introduced in one version vs the other"
  ],
  "negotiation_advice": "Actionable strategy for which terms to push back on or accept."
}
"""

def compare_legal_documents(
    contract_a: str, contract_b: str, name_a: str = "Contract A", name_b: str = "Contract B", force_mock: bool = False
) -> CompareResponse:
    if force_mock or not HAS_GEMINI_KEY:
        return get_mock_comparison(contract_a, contract_b, name_a, name_b)

    try:
        from google import genai
        client = genai.Client(api_key=GEMINI_API_KEY)
        
        prompt = (
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
            }
        )

        data = json.loads(response.text)
        data["disclaimer"] = get_standard_disclaimer()
        return CompareResponse(**data)
    except Exception as e:
        logger.warning(f"Live Gemini comparison failed: {e}. Falling back to mock engine.")
        return get_mock_comparison(contract_a, contract_b, name_a, name_b)
