"""Celery tasks related to campaign execution."""

import uuid

from celery import shared_task
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models.campaign import Campaign, CampaignStatus
from app.models.contact import Contact
from app.services.social_service import get_social_service


@shared_task(name="app.workers.tasks_campaigns.run_campaign")
def run_campaign(campaign_id: str) -> str:
    """Execute a campaign by sending messages to contacts.

    This demo task simply iterates over all contacts and logs sending. In a
    production environment segmentation and throttling logic would be applied
    and failures would be retried selectively.
    """

    db: Session = SessionLocal()
    try:
        campaign = db.get(Campaign, uuid.UUID(campaign_id))
        if not campaign:
            return "campaign_not_found"
        campaign.status = CampaignStatus.RUNNING
        social_service = get_social_service()
        contacts = db.scalars(select(Contact)).all()
        for contact in contacts:
            for channel in campaign.channels:
                destination = contact.email or contact.whatsapp_id or "unknown"
                content = channel.template or campaign.description or ""
                social_service.send_message(channel, destination, content)
        campaign.status = CampaignStatus.COMPLETED
        db.commit()
        return "completed"
    finally:
        db.close()
