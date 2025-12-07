"""Contact source model capturing provenance."""

import uuid
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class SourceType(str, Enum):
    """Enumerates contact acquisition sources."""

    IMPORT_CSV = "IMPORT_CSV"
    META_WEBHOOK = "META_WEBHOOK"
    MANUAL = "MANUAL"
    API = "API"


class ContactSource(Base):
    """Tracks how a contact entered the system for auditing."""

    __tablename__ = "contact_sources"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    contact_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("contacts.id", ondelete="CASCADE"), nullable=False
    )
    source_type: Mapped[SourceType] = mapped_column(Enum(SourceType), nullable=False)
    source_detail: Mapped[str | None] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False
    )

    contact = relationship("Contact", back_populates="sources")
