"""Webhook receiver for email providers."""

import logging
from fastapi import APIRouter, Request, status, HTTPException
from app.workers.tasks_webhooks import process_email_event

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/webhooks/email", status_code=status.HTTP_202_ACCEPTED)
async def receive_email_webhook(request: Request) -> dict[str, str]:
    """Accept email engagement payloads and enqueue background processing."""
    try:
        payload = await request.json()
    except Exception as e:
        logger.warning("Invalid JSON in email webhook: %s", e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid JSON payload"
        )

    # Optional: verify signature or provider-specific headers here
    # Example: validate_sendgrid_signature(request.headers, payload)

    try:
        process_email_event.delay(payload)
    except Exception as e:
        logger.error("Failed to enqueue email event: %s", e)
        # Still return 202 to avoid retries from provider (common practice)
        # but log the error for debugging

    return {"status": "queued"}