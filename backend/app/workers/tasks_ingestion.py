"""Celery tasks for bulk ingestion."""

from contextlib import contextmanager
from typing import List, Dict

from celery import shared_task
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.services.contact_service import ContactService


@contextmanager
def get_db_session():
    """Reusable database session with proper rollback on error."""
    db: Session = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


@shared_task(bind=True, name="app.workers.tasks_ingestion.import_contacts", max_retries=3)
def import_contacts_task(self, rows: List[Dict]) -> int:
    """Normalize and upsert contacts in background."""
    if not isinstance(rows, list):
        raise ValueError("Input must be a list of contact dictionaries")

    with get_db_session() as db:
        try:
            service = ContactService(db)
            contacts = service.bulk_import(rows)
            db.commit()  # Explicit commit after successful import
            return len(contacts)
        except SQLAlchemyError as e:
            db.rollback()
            raise self.retry(exc=e, countdown=60, max_retries=3)
        except Exception as e:
            db.rollback()
            # Re-raise non-SQLAlchemy errors immediately (they won't benefit from retry)
            raise