"""Unified contact model used across channels."""

import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import JSON

from app.db.base import Base


class Contact(Base):
    """Represents a person across multiple channels."""

    __tablename__ = "contacts"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    email: Mapped[str | None] = mapped_column(String(255), unique=True)
    phone: Mapped[str | None] = mapped_column(String(50))
    whatsapp_id: Mapped[str | None] = mapped_column(String(255))
    instagram_id: Mapped[str | None] = mapped_column(String(255))
    facebook_id: Mapped[str | None] = mapped_column(String(255))
    is_opt_in: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    tags: Mapped[dict | None] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow
    )

    sources = relationship("ContactSource", back_populates="contact", cascade="all, delete-orphan")
    interaction_events = relationship(
        "InteractionEvent", back_populates="contact", cascade="all, delete-orphan"
    )
