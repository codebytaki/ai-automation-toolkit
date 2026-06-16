"""Pytest configuration and shared fixtures."""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch


@pytest.fixture(scope="session")
def client():
    """FastAPI test client with DB patched out."""
    with patch("app.core.database.init_db"), \
         patch("app.core.database.close_db"):
        from app.main import app
        with TestClient(app) as c:
            yield c


@pytest.fixture
def auth_headers():
    """Return mock auth headers — use in tests that need authentication."""
    from app.core.security import create_access_token
    token = create_access_token(subject=1)
    return {"Authorization": f"Bearer {token}"}
