import pytest
from fastapi.testclient import TestClient
from backend.app import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "online"
    assert "service" in data

def test_samples_endpoint():
    response = client.get("/api/samples")
    assert response.status_code == 200
    data = response.json()
    assert "samples" in data
    assert len(data["samples"]) >= 3
    for sample in data["samples"]:
        assert "id" in sample
        assert "title" in sample
        assert len(sample["content"]) > 50

def test_analyze_predatory_contract_endpoint():
    payload = {
        "text": (
            "INDEPENDENT CONTRACTOR & INTELLECTUAL PROPERTY ASSIGNMENT AGREEMENT. "
            "Company may terminate upon 24 hours notice. "
            "Contractor agrees to a 36-month non-compete worldwide. "
            "Governing law is Cayman Islands arbitration."
        ),
        "reading_level": "Plain English",
        "force_mock": True
    }
    response = client.post("/api/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["overall_risk_score"] > 50
    assert "High Risk" in data["risk_verdict"]
    assert "risks" in data
    assert len(data["risks"]) >= 3
    assert "clauses" in data
    assert len(data["clauses"]) >= 4
    assert "action_checklist" in data
    assert len(data["action_checklist"]) >= 3
    assert "lawyer_prep" in data
    assert len(data["lawyer_prep"]["questions_to_ask"]) >= 3
    assert "disclaimer" in data

def test_analyze_lease_endpoint():
    payload = {
        "text": (
            "RESIDENTIAL LEASE AGREEMENT. "
            "Rent is $1,850 payable on 1st of month. "
            "Security deposit is $3,700 returned within 30 days. "
            "Either party may terminate with 30 days written notice."
        ),
        "reading_level": "Executive",
        "force_mock": True
    }
    response = client.post("/api/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["overall_risk_score"] < 40
    assert "Favorable" in data["risk_verdict"]

def test_analyze_empty_payload_validation():
    payload = {"text": "   "}
    response = client.post("/api/analyze", json=payload)
    assert response.status_code in [400, 422]

def test_compare_endpoint():
    payload = {
        "contract_a_text": "Mutual NDA with 2 years duration and Delaware law jurisdiction.",
        "contract_b_text": "Revised draft with 5 years duration and $100,000 liquidated damages clause.",
        "name_a": "Standard NDA",
        "name_b": "Revised Draft",
        "force_mock": True
    }
    response = client.post("/api/compare", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "favorability_score_a" in data
    assert data["favorability_score_a"] > data["favorability_score_b"]
    assert "comparisons" in data
    assert len(data["comparisons"]) >= 1
    assert "critical_differences" in data
    assert len(data["critical_differences"]) >= 2
    assert "negotiation_advice" in data

def test_chat_termination_query():
    payload = {
        "document_text": "Clause 3: Company may terminate this Agreement at any time upon 24 hours written electronic notice.",
        "query": "Can they fire or terminate me without notice?",
        "force_mock": True
    }
    response = client.post("/api/chat", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert "24 hours" in data["answer"]
    assert len(data["citations"]) > 0
    assert data["risk_note"] is not None

def test_chat_general_query():
    payload = {
        "document_text": "Clause 1: Scope of work includes cloud engineering and database administration.",
        "query": "What is the general purpose of this contract?",
        "force_mock": True
    }
    response = client.post("/api/chat", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert len(data["follow_up_suggestions"]) > 0

def test_simplify_endpoint():
    payload = {
        "clause_text": "Contractor shall indemnify and hold harmless Company without monetary limit.",
        "reading_level": "Plain English"
    }
    response = client.post("/api/simplify", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "simplified" in data
    assert data["reading_level"] == "Plain English"
