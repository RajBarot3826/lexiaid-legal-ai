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

def test_analyze_endpoint():
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
    assert "risks" in data
    assert "clauses" in data
    assert "action_checklist" in data
    assert "lawyer_prep" in data
    assert "disclaimer" in data

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
    assert "comparisons" in data
    assert len(data["comparisons"]) >= 1

def test_chat_endpoint():
    payload = {
        "document_text": "Clause 3: Company may terminate this Agreement at any time upon 24 hours written electronic notice.",
        "query": "Can they fire or terminate me without notice?",
        "force_mock": True
    }
    response = client.post("/api/chat", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert len(data["citations"]) > 0

def test_simplify_endpoint():
    payload = {
        "clause_text": "Contractor shall indemnify and hold harmless Company without monetary limit.",
        "reading_level": "Plain English"
    }
    response = client.post("/api/simplify", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "simplified" in data
