import pytest
from backend.services.mock_engine import (
    get_mock_analysis,
    get_mock_comparison,
    get_mock_chat_response,
    get_mock_simplification
)

def test_predatory_contract_analysis():
    predatory_sample = "Independent contractor agreement with 36 months non-compete and Cayman Islands arbitration."
    res = get_mock_analysis(predatory_sample)
    assert res.overall_risk_score >= 70
    assert "High Risk" in res.risk_verdict
    assert len(res.risks) >= 3
    assert len(res.clauses) >= 4
    assert res.lawyer_prep is not None
    assert len(res.lawyer_prep.questions_to_ask) >= 3
    assert any("Cayman" in c.original_snippet for c in res.clauses)

def test_lease_contract_analysis():
    lease_sample = "Residential lease agreement with landlord and tenant rent of 1,850."
    res = get_mock_analysis(lease_sample)
    assert res.overall_risk_score < 40
    assert "Favorable" in res.risk_verdict
    assert len(res.action_checklist) >= 3
    assert any("Move-in" in chk.task or "inspection" in chk.task.lower() for chk in res.action_checklist)

def test_general_contract_analysis():
    general_sample = "Standard commercial service agreement between buyer and seller regarding software."
    res = get_mock_analysis(general_sample)
    assert res.overall_risk_score == 45
    assert "Moderate Risk" in res.risk_verdict
    assert len(res.clauses) >= 2
    assert len(res.action_checklist) >= 2

def test_contract_comparison_divergence():
    sample_a = "Standard NDA 2 years duration Delaware law."
    sample_b = "Revised draft 5 years duration liquidated damages 100,000."
    comp = get_mock_comparison(sample_a, sample_b, "Standard", "Revised")
    assert comp.favorability_score_a > comp.favorability_score_b
    assert len(comp.comparisons) >= 3
    assert any("liquidated damages" in diff.lower() for diff in comp.critical_differences)
    assert comp.negotiation_advice is not None

def test_grounded_qa_citations():
    doc_sample = "Clause 3: Company may terminate this Agreement at any time upon 24 hours notice."
    chat_res = get_mock_chat_response("Can they terminate without notice?", doc_sample)
    assert "24 hours" in chat_res.answer
    assert len(chat_res.citations) > 0
    assert "Clause 3" in chat_res.citations[0]
    assert len(chat_res.follow_up_suggestions) >= 2

def test_grounded_qa_lease_rent():
    doc_sample = "Clause 2: Monthly rent is $1,850.00, payable on or before the first day of each month."
    chat_res = get_mock_chat_response("What is the rent?", doc_sample)
    assert "1,850" in chat_res.answer
    assert len(chat_res.citations) > 0

def test_grounded_qa_non_compete():
    doc_sample = "Clause 5: Contractor shall not directly or indirectly engage in enterprise software."
    chat_res = get_mock_chat_response("Is there a non-compete?", doc_sample)
    assert "non-compete" in chat_res.answer.lower()
    assert chat_res.risk_note is not None

def test_clause_simplification():
    clause = "Contractor shall indemnify and hold harmless Company from all liabilities."
    simp = get_mock_simplification(clause)
    assert "plain english" in simp.reading_level.lower()
    assert "Critical" in simp.risk_verdict or "Risk" in simp.risk_verdict
    assert len(simp.key_takeaway) > 5
