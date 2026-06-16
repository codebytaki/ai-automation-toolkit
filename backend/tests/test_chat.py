"""Tests for Multi-AI Chat endpoint."""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch


def test_model_list_structure():
    """Available models dict should have valid entries."""
    from app.api.v1.endpoints.chat import AVAILABLE_MODELS
    assert len(AVAILABLE_MODELS) >= 5
    for key, value in AVAILABLE_MODELS.items():
        assert isinstance(key, str)
        assert "/" in value  # LiteLLM format: provider/model


def test_model_response_schema():
    """ModelResponse should serialize correctly."""
    from app.api.v1.endpoints.chat import ModelResponse
    r = ModelResponse(
        model="gpt-4o-mini",
        text="Hello world",
        tokens_used=42,
        latency_ms=150,
        cost_usd=0.000042,
    )
    assert r.model == "gpt-4o-mini"
    assert r.tokens_used == 42
    assert r.error is None


@pytest.mark.asyncio
async def test_call_model_handles_api_error():
    """_call_model should return error field, not raise, on API failure."""
    from app.api.v1.endpoints.chat import _call_model

    with patch("litellm.acompletion", new_callable=AsyncMock) as mock_llm:
        mock_llm.side_effect = Exception("API rate limited")
        result = await _call_model("gpt-4o-mini", [{"role": "user", "content": "hi"}], 0.7, 100)
        assert result.error is not None
        assert result.text == ""
        assert result.tokens_used == 0
