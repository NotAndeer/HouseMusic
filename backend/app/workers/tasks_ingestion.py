"""Celery tasks for bulk ingestion."""

from celery import shared_task

from app.db.session import SessionLocal
from app.services.contact_service import ContactService


@shared_task(name="app.workers.tasks_ingestion.import_contacts")
def import_contacts_task(rows: list[dict]) -> int:
    """Normalize and upsert contacts in background."""

    db = SessionLocal()
    try:
        service = ContactService(db)
        service.bulk_import(rows)
        return len(rows)
    finally:
        db.close()
