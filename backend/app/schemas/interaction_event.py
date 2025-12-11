"""Pydantic schemas for interaction events."""

import uuid
from datetime import datetime
from typing import Optional, Any

from pydantic import BaseModel

from app.models.interaction_event import InteractionEventType


class InteractionEventOut(BaseModel):
    """Representation of an interaction event returned to API consumers."""
    
    id: uuid.UUID
    contact_id: Optional[uuid.UUID] = None
    event_type: InteractionEventType
    payload_json: Optional[dict[str, Any]] = None
    created_at: datetime

    model_config = {"from_attributes": True}