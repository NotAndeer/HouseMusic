"""Conversation model tracking stateful bot interactions."""

import uuid
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import DateTime, Enum, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class ConversationState(str, Enum):
    """Simple states for the demo chatbot."""

    STEP_1 = "STEP_1"
    STEP_2 = "STEP_2"
    STEP_3 = "STEP_3"


class Channel(str, Enum):
    """Channels supported for bot interactions."""

    EMAIL = "EMAIL"
    WHATSAPP = "WHATSAPP"
    INSTAGRAM = "INSTAGRAM"
    FACEBOOK = "FACEBOOK"


def _utcnow():
    return datetime.now(timezone.utc)


class Conversation(Base):
    """Represents the ongoing dialog with an external user."""

    __tablename__ = "conversations"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    external_user_id: Mapped[str] = mapped_column(String(255), nullable=False)
    state: Mapped[ConversationState] = mapped_column(Enum(ConversationState), nullable=False)
    last_message_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    channel: Mapped[Channel] = mapped_column(Enum(Channel), nullable=False)
    contact_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("contacts.id", ondelete="SET NULL")
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_utcnow, onupdate=_utcnow
    )

    contact = relationship("Contact", back_populates="conversations")