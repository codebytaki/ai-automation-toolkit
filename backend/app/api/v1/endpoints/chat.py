"""Multi-AI Chat endpoint — compare responses from multiple models simultaneously."""

import asyncio
import time
from typing import List, Optional

import litellm
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.api.v1.endpoints.auth import get_current_user
from app.core.config import settings
from app.models.user import User

router = APIRouter()

# Supported models via LiteLLM
AVAILABLE_MODELS = {
    "gpt-4o":             "openai/gpt-4o",
    "gpt-4o-mini":        "openai/gpt-4o-mini",
    "claude-3-5-sonnet":  "anthropic/claude-3-5-sonnet-20241022",
    "claude-3-haiku":     "anthropic/claude-3-haiku-20240307",
    "gemini-1.5-pro":     "gemini/gemini-1.5-pro",
    "gemini-1.5-flash":   "gemini/gemini-1.5-flash",
    "groq-llama3":        "groq/llama-3.3-70b-versatile",
    "groq-mixtral":       "groq/mixtral-8x7b-32768",
    "mistral-large":      "mistral/mistral-large-latest",
    "deepseek-chat":      "openrouter/deepseek/deepseek-chat",
}


class ChatMessage(BaseModel):
    role: str  # "user" | "assistant" | "system"
    content: str


class SingleChatRequest(BaseModel):
    model: str = "gpt-4o-mini"
    messages: List[ChatMessage]
    temperature: float = 0.7
    max_tokens: int = 1024
    system_prompt: Optional[str] = None


class MultiChatRequest(BaseModel):
    models: List[str] = ["gpt-4o-mini", "claude-3-haiku", "groq-llama3"]
    prompt: str
    system_prompt: Optional[str] = None
    temperature: float = 0.7
    max_tokens: int = 1024


class ModelResponse(BaseModel):
    model: str
    text: str
    tokens_used: int
    latency_ms: int
    cost_usd: float
    error: Optional[str] = None


async def _call_model(model_key: str, messages: list, temperature: float, max_tokens: int) -> ModelResponse:
    """Call a single model and return structured response."""
    model_path = AVAILABLE_MODELS.get(model_key, model_key)
    start = time.monotonic()
    try:
        response = await litellm.acompletion(
            model=model_path,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        latency = int((time.monotonic() - start) * 1000)
        usage = response.usage or {}
        cost = litellm.completion_cost(completion_response=response)
        return ModelResponse(
            model=model_key,
            text=response.choices[0].message.content or "",
            tokens_used=getattr(usage, "total_tokens", 0),
            latency_ms=latency,
            cost_usd=round(cost, 6),
        )
    except Exception as e:
        latency = int((time.monotonic() - start) * 1000)
        return ModelResponse(
            model=model_key, text="", tokens_used=0, latency_ms=latency,
            cost_usd=0.0, error=str(e),
        )


@router.get("/models")
def list_models():
    """List all available AI models."""
    return {"models": list(AVAILABLE_MODELS.keys()), "count": len(AVAILABLE_MODELS)}


@router.post("/send")
async def send_message(
    body: SingleChatRequest,
    current_user: User = Depends(get_current_user),
):
    """Send a message to a single AI model."""
    messages = []
    if body.system_prompt:
        messages.append({"role": "system", "content": body.system_prompt})
    messages.extend([{"role": m.role, "content": m.content} for m in body.messages])

    result = await _call_model(body.model, messages, body.temperature, body.max_tokens)
    return result


@router.post("/compare")
async def compare_models(
    body: MultiChatRequest,
    current_user: User = Depends(get_current_user),
):
    """Send one prompt to multiple models simultaneously and compare results."""
    # Validate models
    for m in body.models:
        if m not in AVAILABLE_MODELS:
            raise HTTPException(status_code=400, detail=f"Unknown model: {m}")

    messages = []
    if body.system_prompt:
        messages.append({"role": "system", "content": body.system_prompt})
    messages.append({"role": "user", "content": body.prompt})

    # Execute all models in parallel
    tasks = [
        _call_model(m, messages, body.temperature, body.max_tokens)
        for m in body.models
    ]
    results = await asyncio.gather(*tasks)

    # Sort by latency
    sorted_results = sorted(results, key=lambda r: r.latency_ms)
    total_cost = sum(r.cost_usd for r in results)

    return {
        "prompt": body.prompt,
        "responses": sorted_results,
        "total_cost_usd": round(total_cost, 6),
        "fastest_model": sorted_results[0].model if sorted_results else None,
        "models_compared": len(body.models),
    }
