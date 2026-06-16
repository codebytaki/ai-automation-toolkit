"""Agent and AgentRun database models."""

from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, JSON, ForeignKey
from app.core.database import Base


class Agent(Base):
    __tablename__ = "agents"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, default="")
    system_prompt = Column(Text, nullable=False)
    model = Column(String(50), default="gpt-4o-mini")
    tools = Column(JSON, default=list)           # list of tool names
    memory_type = Column(String(20), default="conversation")
    temperature = Column(Float, default=0.7)
    max_tokens = Column(Integer, default=2048)
    is_active = Column(Boolean, default=True)
    run_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class AgentRun(Base):
    __tablename__ = "agent_runs"

    id = Column(Integer, primary_key=True, index=True)
    agent_id = Column(Integer, ForeignKey("agents.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    input = Column(Text, nullable=False)
    output = Column(Text, nullable=True)
    error = Column(Text, nullable=True)
    status = Column(String(20), default="queued")   # queued | running | completed | failed
    tokens_used = Column(Integer, default=0)
    cost_usd = Column(Float, default=0.0)
    started_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    completed_at = Column(DateTime(timezone=True), nullable=True)
