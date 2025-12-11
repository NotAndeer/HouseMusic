"""Celery tasks related to campaign execution."""

import uuid
from contextlib import contextmanager

from celery import shared_task
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models.campaign import Campaign, CampaignStatus
from app.models.contact import Contact
from app.services.social_service import get_social_service


@contextmanager
def get_db_session():
    """Reusable DB session context manager for tasks."""
    db: Session = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


@shared_task(bind=True, name="app.workers.tasks_campaigns.run_campaign", max_retries=3)
def run_campaign(self, campaign_id: str) -> str:
    """Execute a campaign by sending messages to contacts.

    This demo task iterates over all contacts and sends messages per channel.
    In production, segmentation, throttling, and per-contact error handling
    would be applied.
    """
    try:
        campaign_uuid = uuid.UUID(campaign_id)
    except ValueError:
        return "invalid_campaign_id"

    with get_db_session() as db:
        campaign = db.get(Campaign, campaign_uuid)
        if not campaign:
            return "campaign_not_found"

        if campaign.status != CampaignStatus.SCHEDULED:
            return "campaign_not_scheduled"

        # Update status to RUNNING
        campaign.status = CampaignStatus.RUNNING
        db.commit()  # Commit early to reflect status change

        social_service = get_social_service()
        contacts = db.scalars(select(Contact)).all()

        success_count = 0
        for contact in contacts:
            try:
                for channel in campaign.channels:
                    # Determine destination per channel
                    if channel.channel_type == "EMAIL":
                        destination = contact.email
                    elif channel.channel_type == "WHATSAPP":
                        destination = contact.whatsapp_id
                    elif channel.channel_type in ("INSTAGRAM", "FACEBOOK"):
                        destination = contact.instagram_id or contact.facebook_id
                    else:
                        destination = None

                    if not destination:
                        continue  # Skip if no destination for this channel

                    content = channel.template or campaign.description or ""
                    sent = social_service.send_message(channel, destination, content)
                    if sent:
                        success_count += 1

            except Exception as e:
                # Log error but continue with next contact
                # In production: log to monitoring system
                pass

        # Mark as completed
        campaign.status = CampaignStatus.COMPLETED
        db.commit()

        return f"completed: {success_count} messages sent"