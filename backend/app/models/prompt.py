"""Prompt Library database model."""

from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, JSON, ForeignKey
from app.core.database import Base


class Prompt(Base):
    __tablename__ = "prompts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    category = Column(String(50), default="other", index=True)
    description = Column(Text, default="")
    tags = Column(JSON, default=list)
    is_public = Column(Boolean, default=False)
    use_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc),
                        onupdate=lambda: datetime.now(timezone.utc))
