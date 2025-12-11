"""Social account model linking users to external providers."""

import enum
import uuid
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import DateTime, Enum, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class SocialProvider(str, enum.Enum):
    """Supported social providers."""

    FACEBOOK = "FACEBOOK"
    INSTAGRAM = "INSTAGRAM"
    WHATSAPP = "WHATSAPP"
    GMAIL = "GMAIL"


def _utcnow():
    return datetime.now(timezone.utc)


class SocialAccount(Base):
    """Represents an OAuth connection to an external social provider.

    Access and refresh tokens are stored encrypted. In production a KMS or
    vault-backed encryption scheme should be used; this model only exposes
    fields for the encrypted blobs and expiration metadata.
    """

    __tablename__ = "social_accounts"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    provider: Mapped[SocialProvider] = mapped_column(Enum(SocialProvider), nullable=False)
    access_token_encrypted: Mapped[str] = mapped_column(String(512), nullable=False)
    refresh_token_encrypted: Mapped[Optional[str]] = mapped_column(String(512))
    expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    external_id: Mapped[Optional[str]] = mapped_column(String(255))
    display_name: Mapped[Optional[str]] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_utcnow, onupdate=_utcnow
    )

    user = relationship("User", back_populates="social_accounts")