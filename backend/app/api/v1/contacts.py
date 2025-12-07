"""Contact management endpoints."""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.contact import Contact
from app.schemas.contact import ContactCreate, ContactOut, ContactUpdate
from app.services.contact_service import ContactService, get_contact_service

router = APIRouter()


@router.get("/contacts", response_model=list[ContactOut])
def list_contacts(
    *,
    db: Session = Depends(get_db),
    email: str | None = Query(default=None),
    tag: str | None = Query(default=None),
    is_opt_in: bool | None = Query(default=None),
    skip: int = 0,
    limit: int = 20,
) -> list[Contact]:
    """Return a paginated list of contacts with optional filters."""

    query = select(Contact)
    if email:
        query = query.where(Contact.email == email)
    if tag:
        query = query.where(Contact.tags.contains({tag: True}))
    if is_opt_in is not None:
        query = query.where(Contact.is_opt_in == is_opt_in)
    contacts = db.scalars(query.offset(skip).limit(limit)).all()
    return contacts


@router.post("/contacts", response_model=ContactOut, status_code=status.HTTP_201_CREATED)
def create_contact(
    payload: ContactCreate,
    contact_service: ContactService = Depends(get_contact_service),
) -> Contact:
    """Create a new contact or update existing one based on email/social ids."""

    return contact_service.create_or_update_contact(email=payload.email, payload=payload.model_dump())


@router.get("/contacts/{contact_id}", response_model=ContactOut)
def get_contact(contact_id: str, db: Session = Depends(get_db)) -> Contact:
    """Retrieve a single contact by identifier."""

    contact = db.get(Contact, contact_id)
    if not contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.put("/contacts/{contact_id}", response_model=ContactOut)
def update_contact(
    contact_id: str,
    payload: ContactUpdate,
    db: Session = Depends(get_db),
) -> Contact:
    """Update contact fields."""

    contact = db.get(Contact, contact_id)
    if not contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(contact, field, value)
    db.commit()
    db.refresh(contact)
    return contact


@router.post("/contacts/import", response_model=list[ContactOut])
def import_contacts(
    contacts: list[ContactCreate],
    contact_service: ContactService = Depends(get_contact_service),
) -> list[Contact]:
    """Bulk import contacts from JSON payload. CSV hooks could be added later."""

    payloads = [contact.model_dump() for contact in contacts]
    return contact_service.bulk_import(payloads)
