import json
import logging
from typing import List, Optional
from ..config import GEMINI_API_KEY, DEFAULT_MODEL, HAS_GEMINI_KEY
from ..models.schemas import ChatResponse, ChatMessage
from ..utils.security import get_standard_disclaimer
from .mock_engine import get_mock_chat_response

logger = logging.getLogger("lexiaid.chat")

CHAT_SYSTEM_PROMPT = """You are LexiAid's Grounded Legal Document Q&A Agent.
Your objective is to answer user questions accurately based STRICTLY on the text of the provided legal document.

Rules:
1. Always base your response directly on the provided document text. Do not hallucinate external clauses.
2. Provide exact verbatim citations / quotes from the document to support your answer.
3. If an answer cannot be determined from the document, explicitly state: "The provided document does not mention this matter."
4. If the clause in question contains severe legal risks for the user, highlight it in the risk_note.
5. Provide 2-3 logical follow-up questions the user might want to ask.

Output a valid JSON object matching:
{
  "answer": "Clear, accessible, direct answer in plain English.",
  "citations": ["Exact quote 1 from document", "Exact quote 2 from document"],
  "risk_note": "Optional highlight of any dangerous terms or legal traps in this clause",
  "follow_up_suggestions": ["Suggested question 1", "Suggested question 2"]
}
"""

def answer_legal_query(
    query: str, document_text: str, history: Optional[List[ChatMessage]] = None, force_mock: bool = False
) -> ChatResponse:
    if force_mock or not HAS_GEMINI_KEY:
        return get_mock_chat_response(query, document_text)

    try:
        from google import genai
        client = genai.Client(api_key=GEMINI_API_KEY)
        
        prompt = (
            f"Document Text:\n\"\"\"\n{document_text}\n\"\"\"\n\n"
            f"User Question: {query}\n"
        )
        
        response = client.models.generate_content(
            model=DEFAULT_MODEL,
            contents=prompt,
            config={
                "system_instruction": CHAT_SYSTEM_PROMPT,
                "response_mime_type": "application/json",
            }
        )

        data = json.loads(response.text)
        data["disclaimer"] = get_standard_disclaimer()
        return ChatResponse(**data)
    except Exception as e:
        logger.warning(f"Live Gemini chat failed: {e}. Falling back to mock engine.")
        return get_mock_chat_response(query, document_text)
