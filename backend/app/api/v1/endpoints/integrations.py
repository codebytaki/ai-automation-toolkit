"""Integrations endpoints — manage and test third-party connections."""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.api.v1.endpoints.auth import get_current_user
from app.models.user import User
from app.services.integration_service import IntegrationService

router = APIRouter()

SUPPORTED = [
    "github", "slack", "discord", "telegram", "notion",
    "google_drive", "gmail", "openai", "anthropic", "stripe",
]


class IntegrationConfig(BaseModel):
    integration: str
    config: dict  # provider-specific config (API key, token, etc.)


@router.get("/")
def list_integrations():
    """List all supported integrations."""
    return {
        "integrations": [
            {"name": "GitHub",       "id": "github",       "category": "developer", "icon": "github"},
            {"name": "Slack",        "id": "slack",        "category": "comm",      "icon": "slack"},
            {"name": "Discord",      "id": "discord",      "category": "comm",      "icon": "discord"},
            {"name": "Telegram",     "id": "telegram",     "category": "comm",      "icon": "telegram"},
            {"name": "Notion",       "id": "notion",       "category": "productivity", "icon": "notion"},
            {"name": "Google Drive", "id": "google_drive", "category": "productivity", "icon": "google"},
            {"name": "Gmail",        "id": "gmail",        "category": "email",     "icon": "gmail"},
            {"name": "OpenAI",       "id": "openai",       "category": "ai",        "icon": "openai"},
            {"name": "Anthropic",    "id": "anthropic",    "category": "ai",        "icon": "anthropic"},
            {"name": "Stripe",       "id": "stripe",       "category": "payment",   "icon": "stripe"},
        ]
    }


@router.post("/test")
async def test_integration(
    body: IntegrationConfig,
    current_user: User = Depends(get_current_user),
):
    """Test if an integration connection is working."""
    if body.integration not in SUPPORTED:
        raise HTTPException(status_code=400, detail=f"Unknown integration: {body.integration}")

    result = await IntegrationService.test(body.integration, body.config)
    return {"integration": body.integration, "status": result["status"], "message": result["message"]}


@router.post("/github/repos")
async def list_github_repos(
    token: str,
    current_user: User = Depends(get_current_user),
):
    """List GitHub repositories using provided token."""
    result = await IntegrationService.github_list_repos(token)
    return result


@router.post("/slack/send")
async def slack_send_message(
    token: str,
    channel: str,
    message: str,
    current_user: User = Depends(get_current_user),
):
    """Send a message to a Slack channel."""
    result = await IntegrationService.slack_send(token, channel, message)
    return result


@router.post("/notion/pages")
async def list_notion_pages(
    api_key: str,
    current_user: User = Depends(get_current_user),
):
    """List Notion pages using provided API key."""
    result = await IntegrationService.notion_list_pages(api_key)
    return result
