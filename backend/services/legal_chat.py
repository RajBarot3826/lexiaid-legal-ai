"""Grounded legal document Q&A service.

Provides citation-backed answers to user questions, strictly
grounded in the text of the provided legal document.
"""

import json
import logging
from typing import List, Optional

from ..config import DEFAULT_MODEL, GEMINI_API_KEY, HAS_GEMINI_KEY
from ..models.schemas import ChatMessage, ChatResponse
from ..utils.security import get_standard_disclaimer
from .mock_engine import get_mock_chat_response

logger: logging.Logger = logging.getLogger("lexiaid.chat")

CHAT_SYSTEM_PROMPT: str = """You are LexiAid's Grounded Legal Document Q&A Agent.
Answer user questions accurately based STRICTLY on the provided legal document.

Rules:
1. Base responses directly on the provided document text.
2. Provide exact verbatim citations from the document.
3. If an answer cannot be determined, state: "The provided document does not mention this matter."
4. Highlight severe legal risks in risk_note.
5. Provide 2-3 logical follow-up questions.

Output a valid JSON object matching:
{"answer": "", "citations": [], "risk_note": "", "follow_up_suggestions": []}"""


def answer_legal_query(
    query: str,
    document_text: str,
    history: Optional[List[ChatMessage]] = None,
    force_mock: bool = False,
) -> ChatResponse:
    """Answer a legal question grounded in the provided document.

    Args:
        query: The user's natural-language question.
        document_text: Sanitized legal document text for context.
        history: Optional list of prior chat messages for context.
        force_mock: If True, bypass Gemini and use the mock engine.

    Returns:
        A ChatResponse with a grounded answer, citations, and follow-ups.
    """
    if force_mock or not HAS_GEMINI_KEY:
        return get_mock_chat_response(query, document_text)

    try:
        from google import genai

        client = genai.Client(api_key=GEMINI_API_KEY)
        prompt: str = (
            f'Document Text:\n"""\n{document_text}\n"""\n\n'
            f"User Question: {query}\n"
        )

        response = client.models.generate_content(
            model=DEFAULT_MODEL,
            contents=prompt,
            config={
                "system_instruction": CHAT_SYSTEM_PROMPT,
                "response_mime_type": "application/json",
            },
        )

        data: dict = json.loads(response.text)
        data["disclaimer"] = get_standard_disclaimer()
        return ChatResponse(**data)
    except Exception as exc:
        logger.warning(
            "Gemini chat failed: %s. Falling back to mock engine.", exc
        )
        return get_mock_chat_response(query, document_text)
