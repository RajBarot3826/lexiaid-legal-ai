"""API endpoint integration tests for the LexiAid legal analysis platform.

Covers health checks, sample retrieval, document analysis, contract comparison,
grounded Q&A chat, clause simplification, edge cases, and performance.
"""

import time

import pytest
from fastapi.testclient import TestClient

from backend.app import app

client = TestClient(app)


# ---------------------------------------------------------------------------
# Health & Infrastructure
# ---------------------------------------------------------------------------
class TestHealthEndpoint:
    """Tests for the /api/health endpoint."""

    def test_health_returns_200_with_service_metadata(self) -> None:
        """Health endpoint should return 200 with service name, version, and mode."""
        response = client.get("/api/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "online"
        assert data["service"] == "LexiAid Legal Intelligence API"
        assert data["version"] == "1.0.0"
        assert "gemini_active" in data
        assert "default_model" in data
        assert "mode" in data

    def test_health_includes_processing_time_header(self) -> None:
        """Health response should include X-Processing-Time-Ms header."""
        response = client.get("/api/health")
        assert "X-Processing-Time-Ms" in response.headers
        processing_time = float(response.headers["X-Processing-Time-Ms"])
        assert processing_time < 500  # Should be fast


# ---------------------------------------------------------------------------
# Sample Contracts
# ---------------------------------------------------------------------------
class TestSamplesEndpoint:
    """Tests for the /api/samples endpoint."""

    def test_samples_returns_at_least_three_contracts(self) -> None:
        """Sample endpoint should return at least 3 pre-loaded contracts."""
        response = client.get("/api/samples")
        assert response.status_code == 200
        data = response.json()
        assert "samples" in data
        assert len(data["samples"]) >= 3

    def test_each_sample_has_required_fields(self) -> None:
        """Each sample contract must have id, title, and non-empty content."""
        data = client.get("/api/samples").json()
        for sample in data["samples"]:
            assert "id" in sample
            assert "title" in sample
            assert "content" in sample
            assert len(sample["content"]) > 50


# ---------------------------------------------------------------------------
# Document Analysis
# ---------------------------------------------------------------------------
class TestAnalyzeEndpoint:
    """Tests for the /api/analyze endpoint."""

    def test_predatory_contract_returns_high_risk_with_full_structure(self) -> None:
        """Predatory freelance contract should score >50 risk with risks, clauses, checklist."""
        payload = {
            "text": (
                "INDEPENDENT CONTRACTOR & INTELLECTUAL PROPERTY ASSIGNMENT AGREEMENT. "
                "Company may terminate upon 24 hours notice. "
                "Contractor agrees to a 36-month non-compete worldwide. "
                "Governing law is Cayman Islands arbitration."
            ),
            "reading_level": "Plain English",
            "force_mock": True,
        }
        response = client.post("/api/analyze", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["overall_risk_score"] > 50
        assert "High Risk" in data["risk_verdict"]
        assert len(data["risks"]) >= 3
        assert len(data["clauses"]) >= 4
        assert len(data["action_checklist"]) >= 3
        assert len(data["lawyer_prep"]["questions_to_ask"]) >= 3
        assert "disclaimer" in data

    def test_lease_contract_returns_favorable_risk(self) -> None:
        """Residential lease should score <40 risk with Favorable verdict."""
        payload = {
            "text": (
                "RESIDENTIAL LEASE AGREEMENT. "
                "Rent is $1,850 payable on 1st of month. "
                "Security deposit is $3,700 returned within 30 days. "
                "Either party may terminate with 30 days written notice."
            ),
            "reading_level": "Executive",
            "force_mock": True,
        }
        response = client.post("/api/analyze", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["overall_risk_score"] < 40
        assert "Favorable" in data["risk_verdict"]

    def test_empty_text_returns_validation_error(self) -> None:
        """Empty whitespace-only text should return 400 or 422."""
        response = client.post("/api/analyze", json={"text": "   "})
        assert response.status_code in [400, 422]

    def test_missing_text_field_returns_422(self) -> None:
        """Missing required 'text' field should return 422 validation error."""
        response = client.post("/api/analyze", json={})
        assert response.status_code == 422

    @pytest.mark.parametrize(
        "reading_level",
        ["Plain English", "Executive", "ELI5"],
    )
    def test_all_reading_levels_produce_valid_response(
        self, reading_level: str
    ) -> None:
        """Each reading level should produce a valid analysis response."""
        payload = {
            "text": "Standard commercial lease agreement between landlord and tenant for residential unit.",
            "reading_level": reading_level,
            "force_mock": True,
        }
        response = client.post("/api/analyze", json=payload)
        assert response.status_code == 200
        assert "overall_risk_score" in response.json()

    def test_unicode_document_text_handled_correctly(self) -> None:
        """Documents with unicode characters should process without errors."""
        payload = {
            "text": (
                "Contrat de location résidentielle entre le propriétaire "
                "et le locataire. Loyer mensuel de 1.850€. "
                "Le dépôt de garantie est de 3.700€ — remboursable sous 30 jours."
            ),
            "force_mock": True,
        }
        response = client.post("/api/analyze", json=payload)
        assert response.status_code == 200

    def test_very_long_document_is_accepted_and_analyzed(self) -> None:
        """Documents up to the character limit should be accepted."""
        payload = {
            "text": "This is a standard legal agreement clause. " * 500,
            "force_mock": True,
        }
        response = client.post("/api/analyze", json=payload)
        assert response.status_code == 200

    def test_analysis_response_time_under_two_seconds(self) -> None:
        """Mock analysis should complete in under 2 seconds."""
        payload = {
            "text": "Independent contractor agreement with Cayman Islands arbitration.",
            "force_mock": True,
        }
        start = time.monotonic()
        response = client.post("/api/analyze", json=payload)
        elapsed = time.monotonic() - start
        assert response.status_code == 200
        assert elapsed < 2.0, f"Analysis took {elapsed:.2f}s, expected < 2.0s"


# ---------------------------------------------------------------------------
# Contract Comparison
# ---------------------------------------------------------------------------
class TestCompareEndpoint:
    """Tests for the /api/compare endpoint."""

    def test_comparison_returns_favorability_scores_and_divergences(self) -> None:
        """Comparison should return scores, comparisons, and critical differences."""
        payload = {
            "contract_a_text": "Mutual NDA with 2 years duration and Delaware law jurisdiction.",
            "contract_b_text": "Revised draft with 5 years duration and $100,000 liquidated damages clause.",
            "name_a": "Standard NDA",
            "name_b": "Revised Draft",
            "force_mock": True,
        }
        response = client.post("/api/compare", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["favorability_score_a"] > data["favorability_score_b"]
        assert len(data["comparisons"]) >= 1
        assert len(data["critical_differences"]) >= 2
        assert data["negotiation_advice"]

    def test_comparison_with_missing_contract_b_returns_error(self) -> None:
        """Omitting contract B text should return a validation error."""
        payload = {
            "contract_a_text": "Standard NDA with Delaware jurisdiction.",
        }
        response = client.post("/api/compare", json=payload)
        assert response.status_code == 422


# ---------------------------------------------------------------------------
# Grounded Q&A Chat
# ---------------------------------------------------------------------------
class TestChatEndpoint:
    """Tests for the /api/chat endpoint."""

    def test_termination_query_returns_grounded_answer_with_citations(self) -> None:
        """Termination question should cite the 24-hour notice clause."""
        payload = {
            "document_text": "Clause 3: Company may terminate this Agreement at any time upon 24 hours written electronic notice.",
            "query": "Can they fire or terminate me without notice?",
            "force_mock": True,
        }
        response = client.post("/api/chat", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert "24 hours" in data["answer"]
        assert len(data["citations"]) > 0
        assert data["risk_note"] is not None

    def test_general_query_returns_follow_up_suggestions(self) -> None:
        """General questions should return follow-up suggestions."""
        payload = {
            "document_text": "Clause 1: Scope of work includes cloud engineering and database administration.",
            "query": "What is the general purpose of this contract?",
            "force_mock": True,
        }
        response = client.post("/api/chat", json=payload)
        assert response.status_code == 200
        assert len(response.json()["follow_up_suggestions"]) > 0

    def test_chat_with_empty_document_returns_error(self) -> None:
        """Chat with empty document text should return 400 or 422."""
        payload = {
            "document_text": "   ",
            "query": "What is the notice period?",
        }
        response = client.post("/api/chat", json=payload)
        assert response.status_code in [400, 422]


# ---------------------------------------------------------------------------
# Clause Simplification
# ---------------------------------------------------------------------------
class TestSimplifyEndpoint:
    """Tests for the /api/simplify endpoint."""

    def test_indemnification_clause_simplified_as_critical(self) -> None:
        """Indemnification clause should be simplified and flagged as critical."""
        payload = {
            "clause_text": "Contractor shall indemnify and hold harmless Company without monetary limit.",
            "reading_level": "Plain English",
        }
        response = client.post("/api/simplify", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert "simplified" in data
        assert data["reading_level"] == "Plain English"
        assert "Critical" in data["risk_verdict"]

    def test_generic_clause_simplified_as_moderate(self) -> None:
        """A generic clause should be simplified with moderate risk."""
        payload = {
            "clause_text": "Both parties agree to act in good faith during the performance of this agreement.",
        }
        response = client.post("/api/simplify", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert "Safe" in data["risk_verdict"] or "Moderate" in data["risk_verdict"]


# ---------------------------------------------------------------------------
# Security Headers
# ---------------------------------------------------------------------------
class TestSecurityHeaders:
    """Tests for security hardening headers on all responses."""

    def test_x_content_type_options_header_is_nosniff(self) -> None:
        """All responses should include X-Content-Type-Options: nosniff."""
        response = client.get("/api/health")
        assert response.headers.get("X-Content-Type-Options") == "nosniff"

    def test_x_frame_options_header_is_deny(self) -> None:
        """All responses should include X-Frame-Options: DENY to prevent clickjacking."""
        response = client.get("/api/health")
        assert response.headers.get("X-Frame-Options") == "DENY"

    def test_referrer_policy_header_is_set(self) -> None:
        """All responses should include a Referrer-Policy header."""
        response = client.get("/api/health")
        assert "Referrer-Policy" in response.headers

    def test_processing_time_header_is_numeric(self) -> None:
        """X-Processing-Time-Ms should be a valid positive number."""
        response = client.get("/api/health")
        time_ms = float(response.headers["X-Processing-Time-Ms"])
        assert time_ms >= 0

