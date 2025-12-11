"""Adapters to external social/email providers."""

import logging
from typing import Optional

from app.models.campaign import CampaignChannel, ChannelType

logger = logging.getLogger(__name__)


class SocialService:
    """Facade hiding provider-specific message sending APIs."""

    def send_message(self, channel: CampaignChannel, destination: str, content: str) -> bool:
        """Send a message through the configured channel.
        
        Returns True if the message was successfully dispatched (or enqueued).
        """
        try:
            if channel.channel_type == ChannelType.EMAIL:
                subject = channel.subject or "No subject"
                self._send_email(destination, subject, content)
            elif channel.channel_type == ChannelType.WHATSAPP:
                self._send_whatsapp(destination, content)
            elif channel.channel_type in (ChannelType.INSTAGRAM, ChannelType.FACEBOOK):
                self._send_messenger(destination, content)
            else:
                logger.warning("Unsupported channel type: %s", channel.channel_type)
                return False

            logger.info(
                "Message sent via %s to %s",
                channel.channel_type.value,
                destination,
            )
            return True
        except Exception as e:
            logger.error(
                "Failed to send message via %s to %s: %s",
                channel.channel_type.value,
                destination,
                e,
            )
            raise

    def _send_email(self, destination: str, subject: str, body: str) -> None:
        """Simulate sending an email."""
        # In production: use SMTP, SendGrid, etc.
        logger.debug("EMAIL to %s | Subject: %s | Body: %s", destination, subject, body)

    def _send_whatsapp(self, destination: str, content: str) -> None:
        """Simulate sending a WhatsApp message."""
        # In production: use Meta Cloud API, Twilio, etc.
        logger.debug("WHATSAPP to %s | Message: %s", destination, content)

    def _send_messenger(self, destination: str, content: str) -> None:
        """Simulate sending an Instagram/Facebook message."""
        # In production: use Meta Graph API
        logger.debug("MESSENGER (%s) to %s | Message: %s", destination.split(':')[0], destination, content)


def get_social_service() -> SocialService:
    """Dependency provider used by workers or services."""
    return SocialService()