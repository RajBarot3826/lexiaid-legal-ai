"""Unit tests for LexiAid legal analysis services.

Covers the deterministic mock engine for document analysis, contract
comparison, grounded Q&A, and clause simplification.
"""

import pytest

from backend.services.mock_engine import (
    get_mock_analysis,
    get_mock_chat_response,
    get_mock_comparison,
    get_mock_simplification,
)


# ---------------------------------------------------------------------------
# Document Analysis (Mock Engine)
# ---------------------------------------------------------------------------
class TestMockAnalysis:
    """Tests for the deterministic document analysis engine."""

    def test_predatory_freelance_returns_high_risk_with_detailed_breakdown(self) -> None:
        """Predatory contractor agreement should score >=70 with risks and clauses."""
        res = get_mock_analysis(
            "Independent contractor agreement with 36 months non-compete and Cayman Islands arbitration."
        )
        assert res.overall_risk_score >= 70
        assert "High Risk" in res.risk_verdict
        assert len(res.risks) >= 3
        assert len(res.clauses) >= 4
        assert res.lawyer_prep is not None
        assert len(res.lawyer_prep.questions_to_ask) >= 3
        assert any("Cayman" in c.original_snippet for c in res.clauses)

    def test_residential_lease_returns_favorable_with_checklist(self) -> None:
        """Lease agreement should score <40 with 'Favorable' verdict and checklist."""
        res = get_mock_analysis(
            "Residential lease agreement with landlord and tenant rent of 1,850."
        )
        assert res.overall_risk_score < 40
        assert "Favorable" in res.risk_verdict
        assert len(res.action_checklist) >= 3
        assert any(
            "Move-in" in chk.task or "inspection" in chk.task.lower()
            for chk in res.action_checklist
        )

    def test_general_contract_returns_moderate_risk(self) -> None:
        """Unrecognized contract type should default to moderate risk (score 45)."""
        res = get_mock_analysis(
            "Standard commercial service agreement between buyer and seller regarding software."
        )
        assert res.overall_risk_score == 45
        assert "Moderate Risk" in res.risk_verdict
        assert len(res.clauses) >= 2
        assert len(res.action_checklist) >= 2

    def test_analysis_always_includes_disclaimer(self) -> None:
        """Every analysis response must include a legal disclaimer."""
        res = get_mock_analysis("Any contract text about landlord and tenant.")
        assert "does not provide formal legal advice" in res.disclaimer

    @pytest.mark.parametrize(
        "keyword,expected_verdict",
        [
            ("cayman islands", "High Risk"),
            ("independent contractor", "High Risk"),
            ("lease", "Favorable"),
            ("tenant", "Favorable"),
            ("landlord", "Favorable"),
        ],
    )
    def test_keyword_detection_routes_to_correct_analysis(
        self, keyword: str, expected_verdict: str
    ) -> None:
        """Specific keywords should trigger the correct analysis template."""
        res = get_mock_analysis(f"Agreement containing {keyword} clauses and terms.")
        assert expected_verdict in res.risk_verdict


# ---------------------------------------------------------------------------
# Contract Comparison (Mock Engine)
# ---------------------------------------------------------------------------
class TestMockComparison:
    """Tests for the deterministic contract comparison engine."""

    def test_comparison_returns_higher_favorability_for_standard_contract(self) -> None:
        """Standard NDA should score higher than a revised predatory draft."""
        comp = get_mock_comparison(
            "Standard NDA 2 years duration Delaware law.",
            "Revised draft 5 years duration liquidated damages 100,000.",
            "Standard",
            "Revised",
        )
        assert comp.favorability_score_a > comp.favorability_score_b
        assert len(comp.comparisons) >= 3

    def test_comparison_surfaces_liquidated_damages_as_critical(self) -> None:
        """Liquidated damages should appear in critical_differences."""
        comp = get_mock_comparison("NDA A", "NDA B", "A", "B")
        assert any(
            "liquidated damages" in diff.lower()
            for diff in comp.critical_differences
        )

    def test_comparison_includes_negotiation_advice(self) -> None:
        """Comparison result must include actionable negotiation advice."""
        comp = get_mock_comparison("Contract A", "Contract B")
        assert comp.negotiation_advice is not None
        assert len(comp.negotiation_advice) > 20


# ---------------------------------------------------------------------------
# Grounded Q&A (Mock Engine)
# ---------------------------------------------------------------------------
class TestMockChat:
    """Tests for the deterministic grounded Q&A engine."""

    def test_termination_query_returns_clause_citation(self) -> None:
        """Termination question should cite Clause 3 with 24-hour notice."""
        res = get_mock_chat_response(
            "Can they terminate without notice?",
            "Clause 3: Company may terminate this Agreement at any time upon 24 hours notice.",
        )
        assert "24 hours" in res.answer
        assert len(res.citations) > 0
        assert "Clause 3" in res.citations[0]
        assert len(res.follow_up_suggestions) >= 2

    def test_rent_query_returns_financial_details(self) -> None:
        """Rent question should return monthly amount and citation."""
        res = get_mock_chat_response(
            "What is the rent?",
            "Clause 2: Monthly rent is $1,850.00, payable on or before the first day of each month.",
        )
        assert "1,850" in res.answer
        assert len(res.citations) > 0

    def test_non_compete_query_returns_risk_note(self) -> None:
        """Non-compete question should include a risk note."""
        res = get_mock_chat_response(
            "Is there a non-compete?",
            "Clause 5: Contractor shall not directly or indirectly engage in enterprise software.",
        )
        assert "non-compete" in res.answer.lower()
        assert res.risk_note is not None

    def test_general_query_returns_document_excerpt_citation(self) -> None:
        """Unrecognized queries should still return a document excerpt citation."""
        res = get_mock_chat_response(
            "What color is the sky?",
            "This agreement governs the supply of widgets.",
        )
        assert len(res.citations) > 0
        assert "Document Excerpt" in res.citations[0]


# ---------------------------------------------------------------------------
# Clause Simplification (Mock Engine)
# ---------------------------------------------------------------------------
class TestMockSimplification:
    """Tests for the deterministic clause simplification engine."""

    def test_indemnification_clause_flagged_as_critical(self) -> None:
        """Indemnification clauses should be simplified with Critical risk."""
        res = get_mock_simplification(
            "Contractor shall indemnify and hold harmless Company from all liabilities."
        )
        assert "plain english" in res.reading_level.lower()
        assert "Critical" in res.risk_verdict
        assert len(res.key_takeaway) > 5

    def test_generic_clause_flagged_as_safe_or_moderate(self) -> None:
        """Non-indemnification clauses should default to Safe/Moderate."""
        res = get_mock_simplification(
            "Both parties agree to collaborate in good faith."
        )
        assert "Safe" in res.risk_verdict or "Moderate" in res.risk_verdict
