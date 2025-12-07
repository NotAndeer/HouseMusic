"""Contact domain service handling normalization and upserts."""

from __future__ import annotations

from typing import Iterable

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.contact import Contact
from app.models.contact_source import ContactSource, SourceType


class ContactService:
    """Encapsulates contact creation/update logic to keep routers thin."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def create_or_update_contact(
        self, *, email: str | None, payload: dict, source: SourceType = SourceType.API
    ) -> Contact:
        """Create or update a contact using email/social ids as unique keys."""

        contact = None
        if email:
            contact = self.db.scalar(select(Contact).where(Contact.email == email))
        if not contact and payload.get("whatsapp_id"):
            contact = self.db.scalar(select(Contact).where(Contact.whatsapp_id == payload["whatsapp_id"]))

        if contact:
            for field, value in payload.items():
                setattr(contact, field, value)
        else:
            contact = Contact(email=email, **payload)
            self.db.add(contact)

        self.db.flush()
        if not any(src.source_type == source for src in contact.sources):
            contact.sources.append(
                ContactSource(source_type=source, source_detail="auto", contact_id=contact.id)
            )
        self.db.commit()
        self.db.refresh(contact)
        return contact

    def bulk_import(self, contacts: Iterable[dict]) -> list[Contact]:
        """Import contacts in bulk and return the persisted records."""

        results: list[Contact] = []
        for entry in contacts:
            email = entry.get("email")
            payload = {k: v for k, v in entry.items() if k != "email"}
            results.append(self.create_or_update_contact(email=email, payload=payload))
        return results


def get_contact_service(db: Session) -> ContactService:
    """Dependency factory used by routers and background tasks."""

    return ContactService(db)
