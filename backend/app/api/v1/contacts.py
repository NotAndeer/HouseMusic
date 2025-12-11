"""Contact management endpoints."""

from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.contact import ContactCreate, ContactOut, ContactUpdate
from app.services.contact_service import ContactService, get_contact_service

router = APIRouter()


@router.get("/contacts", response_model=list[ContactOut])
def list_contacts(
    *,
    contact_service: ContactService = Depends(get_contact_service),
    email: str | None = Query(default=None),
    tag: str | None = Query(default=None),
    is_opt_in: bool | None = Query(default=None),
    skip: int = 0,
    limit: int = 20,
) -> list[ContactOut]:
    """Return a paginated list of contacts with optional filters."""
    contacts = contact_service.get_contacts(
        email=email,
        tag=tag,
        is_opt_in=is_opt_in,
        skip=skip,
        limit=limit,
    )
    return [ContactOut.model_validate(contact) for contact in contacts]


@router.post("/contacts", response_model=ContactOut, status_code=status.HTTP_201_CREATED)
def create_contact(
    payload: ContactCreate,
    contact_service: ContactService = Depends(get_contact_service),
) -> ContactOut:
    """Create a new contact or update existing one based on email/social ids."""
    contact = contact_service.create_or_update_contact(
        email=payload.email,
        payload=payload.model_dump(),
    )
    return ContactOut.model_validate(contact)


@router.get("/contacts/{contact_id}", response_model=ContactOut)
def get_contact(
    contact_id: UUID,
    contact_service: ContactService = Depends(get_contact_service),
) -> ContactOut:
    """Retrieve a single contact by identifier."""
    contact = contact_service.get_contact(contact_id)
    if not contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return ContactOut.model_validate(contact)


@router.put("/contacts/{contact_id}", response_model=ContactOut)
def update_contact(
    contact_id: UUID,
    payload: ContactUpdate,
    contact_service: ContactService = Depends(get_contact_service),
) -> ContactOut:
    """Update contact fields."""
    try:
        contact = contact_service.update_contact(
            contact_id=contact_id,
            update_data=payload.model_dump(exclude_unset=True),
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    return ContactOut.model_validate(contact)


@router.post("/contacts/import", response_model=list[ContactOut])
def import_contacts(
    contacts: list[ContactCreate],
    contact_service: ContactService = Depends(get_contact_service),
) -> list[ContactOut]:
    """Bulk import contacts from JSON payload. CSV hooks could be added later."""
    payloads = [contact.model_dump() for contact in contacts]
    created_contacts = contact_service.bulk_import(payloads)
    return [ContactOut.model_validate(contact) for contact in created_contacts]