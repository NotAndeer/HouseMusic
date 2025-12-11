"""Pydantic schemas for conversations."""

import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.models.conversation import Channel, ConversationState


class ConversationBase(BaseModel):
    """Base fields shared across conversation operations."""
    
    contact_id: Optional[uuid.UUID] = None
    channel: Channel
    state: ConversationState
    last_message_at: Optional[datetime] = None


class ConversationOut(ConversationBase):
    """Representation returned to API consumers."""
    
    id: uuid.UUID

    model_config = {"from_attributes": True}