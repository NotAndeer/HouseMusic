"""Interaction events capturing marketing engagement."""

import enum
import uuid
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import JSON

from app.db.base import Base


class InteractionEventType(str, enum.Enum):
    """Possible engagement events."""

    MESSAGE_RECEIVED = "MESSAGE_RECEIVED"
    EMAIL_OPEN = "EMAIL_OPEN"
    EMAIL_CLICK = "EMAIL_CLICK"
    BOUNCE = "BOUNCE"
    DELIVERY = "DELIVERY"


class InteractionEvent(Base):
    """Stores events for analytics and reporting."""

    __tablename__ = "interaction_events"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    contact_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("contacts.id", ondelete="SET NULL")
    )
    event_type: Mapped[InteractionEventType] = mapped_column(
        Enum(InteractionEventType), nullable=False
    )
    payload_json: Mapped[dict | None] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False
    )

    contact = relationship("Contact", back_populates="interaction_events")
