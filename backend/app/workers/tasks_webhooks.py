"""Background processing for webhook ingestion."""

from celery import shared_task
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models.interaction_event import InteractionEvent, InteractionEventType


@shared_task(name="app.workers.tasks_webhooks.process_meta_event")
def process_meta_event(payload: dict) -> str:
    """Normalize Meta webhook payloads and persist interaction events."""

    db: Session = SessionLocal()
    try:
        db.add(
            InteractionEvent(
                contact_id=None,
                event_type=InteractionEventType.MESSAGE_RECEIVED,
                payload_json=payload,
            )
        )
        db.commit()
        return "stored"
    finally:
        db.close()


@shared_task(name="app.workers.tasks_webhooks.process_email_event")
def process_email_event(payload: dict) -> str:
    """Persist email provider webhook events for analytics."""

    db: Session = SessionLocal()
    try:
        db.add(
            InteractionEvent(
                contact_id=None,
                event_type=InteractionEventType.EMAIL_OPEN,
                payload_json=payload,
            )
        )
        db.commit()
        return "stored"
    finally:
        db.close()
