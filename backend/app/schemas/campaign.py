"""Pydantic schemas for campaigns."""

import uuid
from datetime import datetime

from pydantic import BaseModel

from app.models.campaign import CampaignStatus, ChannelType


class CampaignChannelBase(BaseModel):
    """Base configuration for a campaign channel."""

    channel_type: ChannelType
    subject: str | None = None
    template: str | None = None


class CampaignChannelCreate(CampaignChannelBase):
    pass


class CampaignChannelOut(CampaignChannelBase):
    id: uuid.UUID

    class Config:
        from_attributes = True


class CampaignBase(BaseModel):
    """Shared fields for campaigns."""

    name: str
    description: str | None = None
    status: CampaignStatus = CampaignStatus.DRAFT
    scheduled_at: datetime | None = None


class CampaignCreate(CampaignBase):
    channels: list[CampaignChannelCreate] = []


class CampaignUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    status: CampaignStatus | None = None
    scheduled_at: datetime | None = None


class CampaignOut(CampaignBase):
    id: uuid.UUID
    sent_at: datetime | None = None
    channels: list[CampaignChannelOut] = []

    class Config:
        from_attributes = True
