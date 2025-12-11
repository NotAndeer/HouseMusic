"""Webhook receiver for Meta (Facebook/Instagram/WhatsApp)."""

import hashlib
import hmac
import logging
from fastapi import APIRouter, HTTPException, Query, Request, status

from app.core.config import settings
from app.workers.tasks_webhooks import process_meta_event

router = APIRouter()
logger = logging.getLogger(__name__)


def _verify_meta_signature(payload: bytes, signature: str | None) -> bool:
    """Verify that the request was sent by Meta using the app secret."""
    if not signature:
        return False
    expected_signature = "sha256=" + hmac.new(
        settings.meta_app_secret.encode(),
        payload,
        hashlib.sha256,
    ).hexdigest()
    return hmac.compare_digest(expected_signature, signature)


@router.get("/webhooks/meta")
def verify_webhook(
    hub_mode: str | None = Query(default=None),
    hub_challenge: str | None = Query(default=None),
    hub_verify_token: str | None = Query(default=None),
) -> str:
    """Meta validation endpoint echoes back the challenge token."""
    if (
        hub_mode != "subscribe"
        or not hub_challenge
        or hub_verify_token != settings.meta_verify_token
    ):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid verification request")
    return hub_challenge


@router.post("/webhooks/meta", status_code=status.HTTP_202_ACCEPTED)
async def receive_meta_events(request: Request) -> dict[str, str]:
    """Receive webhook events and enqueue processing tasks.

    The raw payload is forwarded to Celery to decouple heavy parsing from the
    HTTP thread. Contact resolution uses ContactService during batch processing.
    """
    signature = request.headers.get("x-hub-signature-256")
    body = await request.body()

    if not _verify_meta_signature(body, signature):
        logger.warning("Meta webhook signature verification failed")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid signature")

    try:
        payload = await request.json()
    except Exception as e:
        logger.warning("Invalid JSON in Meta webhook: %s", e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid JSON")

    process_meta_event.delay(payload)
    return {"status": "queued"}