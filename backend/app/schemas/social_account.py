"""Pydantic schemas for social accounts."""

import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.models.social_account import SocialProvider


class SocialAccountBase(BaseModel):
    """Base fields for social account operations."""
    
    provider: SocialProvider
    external_id: Optional[str] = None
    display_name: Optional[str] = None
    expires_at: Optional[datetime] = None


class SocialAccountCreate(SocialAccountBase):
    """Schema for creating a social account (used internally during OAuth flow)."""
    
    access_token_encrypted: str
    refresh_token_encrypted: Optional[str] = None


class SocialAccountOut(SocialAccountBase):
    """Representation returned to API consumers."""
    
    id: uuid.UUID
    created_at: datetime

    model_config = {"from_attributes": True}