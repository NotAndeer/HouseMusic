"""Pydantic schemas for contacts."""

import uuid
from typing import Any

from pydantic import BaseModel, Field


class ContactBase(BaseModel):
    """Base fields shared across operations."""

    email: str | None = Field(default=None)
    phone: str | None = None
    whatsapp_id: str | None = None
    instagram_id: str | None = None
    facebook_id: str | None = None
    is_opt_in: bool = True
    tags: dict[str, Any] | None = None


class ContactCreate(ContactBase):
    """Fields required when creating a contact."""

    email: str | None = None


class ContactUpdate(ContactBase):
    """Fields allowed to change after creation."""

    pass


class ContactOut(ContactBase):
    """Representation returned to API consumers."""

    id: uuid.UUID

    class Config:
        from_attributes = True
