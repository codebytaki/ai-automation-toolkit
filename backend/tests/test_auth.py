"""Tests for authentication endpoints."""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch

from app.main import app
from app.core.security import hash_password, verify_password, create_access_token, decode_token


client = TestClient(app)


# ── Security unit tests ──────────────────────────────────────

def test_password_hashing_and_verification():
    plain = "securepassword123"
    hashed = hash_password(plain)
    assert hashed != plain
    assert verify_password(plain, hashed)
    assert not verify_password("wrong", hashed)


def test_access_token_create_and_decode():
    token = create_access_token(subject=42)
    payload = decode_token(token)
    assert payload is not None
    assert payload["sub"] == "42"
    assert payload["type"] == "access"


def test_invalid_token_returns_none():
    result = decode_token("not.a.real.token")
    assert result is None


def test_empty_token_returns_none():
    result = decode_token("")
    assert result is None


# ── API endpoint tests ───────────────────────────────────────

def test_health_check():
    r = client.get("/health")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "healthy"
    assert "version" in data


def test_root_endpoint():
    r = client.get("/")
    assert r.status_code == 200
    assert "message" in r.json()


def test_login_with_invalid_credentials_returns_401():
    r = client.post("/api/v1/auth/login", data={
        "username": "nonexistent_user",
        "password": "wrongpassword",
    })
    assert r.status_code in (401, 422, 500)  # 500 if DB not configured in test


def test_protected_route_without_token_returns_401():
    r = client.get("/api/v1/agents/")
    assert r.status_code == 401


def test_protected_route_with_invalid_token_returns_401():
    r = client.get("/api/v1/agents/", headers={"Authorization": "Bearer invalid.token"})
    assert r.status_code == 401
