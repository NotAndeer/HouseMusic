"""Webhook receiver for Meta (Facebook/Instagram/WhatsApp)."""

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status

from app.services.contact_service import ContactService, get_contact_service
from app.workers.tasks_webhooks import process_meta_event

router = APIRouter()


@router.get("/webhooks/meta")
def verify_webhook(hub_mode: str | None = Query(default=None), hub_challenge: str | None = Query(default=None)) -> str:
    """Meta validation endpoint echoes back the challenge token."""

    if hub_mode != "subscribe" or not hub_challenge:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid verification request")
    return hub_challenge


@router.post("/webhooks/meta", status_code=status.HTTP_202_ACCEPTED)
async def receive_meta_events(
    request: Request, contact_service: ContactService = Depends(get_contact_service)
) -> dict[str, str]:
    """Receive webhook events and enqueue processing tasks.

    The raw payload is forwarded to Celery to decouple heavy parsing from the
    HTTP thread. Contact resolution uses ``ContactService`` when processing the
    batch.
    """

    payload = await request.json()
    process_meta_event.delay(payload)
    return {"status": "queued"}
