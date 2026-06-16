"""Workflow and WorkflowRun database models."""

from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, JSON, ForeignKey, Float
from app.core.database import Base


class Workflow(Base):
    __tablename__ = "workflows"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, default="")
    nodes = Column(JSON, default=list)
    edges = Column(JSON, default=list)
    is_active = Column(Boolean, default=True)
    run_count = Column(Integer, default=0)
    last_run_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class WorkflowRun(Base):
    __tablename__ = "workflow_runs"

    id = Column(Integer, primary_key=True, index=True)
    workflow_id = Column(Integer, ForeignKey("workflows.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    input_data = Column(JSON, default=dict)
    output = Column(Text, nullable=True)
    error = Column(Text, nullable=True)
    status = Column(String(20), default="queued")
    duration_ms = Column(Integer, nullable=True)
    started_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    completed_at = Column(DateTime(timezone=True), nullable=True)
