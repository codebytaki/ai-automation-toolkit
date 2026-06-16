"""API v1 router — aggregates all endpoint modules."""

from fastapi import APIRouter

from app.api.v1.endpoints import auth, agents, workflows, chat, files, prompts, integrations, analytics

api_router = APIRouter()

api_router.include_router(auth.router,         prefix="/auth",         tags=["Auth"])
api_router.include_router(agents.router,       prefix="/agents",       tags=["Agents"])
api_router.include_router(workflows.router,    prefix="/workflows",    tags=["Workflows"])
api_router.include_router(chat.router,         prefix="/chat",         tags=["Multi-AI Chat"])
api_router.include_router(files.router,        prefix="/files",        tags=["File AI"])
api_router.include_router(prompts.router,      prefix="/prompts",      tags=["Prompt Library"])
api_router.include_router(integrations.router, prefix="/integrations", tags=["Integrations"])
api_router.include_router(analytics.router,    prefix="/analytics",    tags=["Analytics"])
