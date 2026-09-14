"""Shared test fixtures and configuration for the LexiAid test suite.

Provides reusable test fixtures including the FastAPI test client,
sample document texts, and common test data to reduce duplication
across test modules.
"""

import pytest
from fastapi.testclient import TestClient

from backend.app import app


@pytest.fixture
def client() -> TestClient:
    """Create a FastAPI test client for integration testing.

    Returns:
        A TestClient instance configured with the LexiAid app.
    """
    return TestClient(app)


@pytest.fixture
def predatory_contract_text() -> str:
    """Return a predatory freelance contract sample text.

    Returns:
        A string containing a predatory independent contractor agreement.
    """
    return (
        "INDEPENDENT CONTRACTOR & INTELLECTUAL PROPERTY ASSIGNMENT AGREEMENT. "
        "Company may terminate upon 24 hours notice. "
        "Contractor agrees to a 36-month non-compete worldwide. "
        "Governing law is Cayman Islands arbitration."
    )


@pytest.fixture
def lease_contract_text() -> str:
    """Return a residential lease agreement sample text.

    Returns:
        A string containing a standard residential lease agreement.
    """
    return (
        "RESIDENTIAL LEASE AGREEMENT. "
        "Rent is $1,850 payable on 1st of month. "
        "Security deposit is $3,700 returned within 30 days. "
        "Either party may terminate with 30 days written notice."
    )
