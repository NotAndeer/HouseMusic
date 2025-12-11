"""Message log for inbound/outbound traffic."""

import enum
import uuid
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import DateTime, Enum, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class MessageDirection(str, enum.Enum):
    """Direction of a message."""

    INBOUND = "INBOUND"
    OUTBOUND = "OUTBOUND"


def _utcnow():
    return datetime.now(timezone.utc)


class MessageLog(Base):
    """Persists every message for audit and debugging."""

    __tablename__ = "message_logs"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    direction: Mapped[MessageDirection] = mapped_column(Enum(MessageDirection), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    channel: Mapped[str] = mapped_column(String(50), nullable=False)
    external_message_id: Mapped[Optional[str]] = mapped_column(String(255))
    conversation_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("conversations.id", ondelete="SET NULL")
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_utcnow, nullable=False
    )

    conversation = relationship("Conversation", back_populates="messages")