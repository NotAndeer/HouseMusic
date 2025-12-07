"""Webhook receiver for email providers."""

from fastapi import APIRouter, Request, status

from app.workers.tasks_webhooks import process_email_event

router = APIRouter()


@router.post("/webhooks/email", status_code=status.HTTP_202_ACCEPTED)
async def receive_email_webhook(request: Request) -> dict[str, str]:
    """Accept email engagement payloads and enqueue background processing."""

    payload = await request.json()
    process_email_event.delay(payload)
    return {"status": "queued"}
