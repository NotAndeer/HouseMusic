"""Adapters to external social/email providers."""

from app.models.campaign import CampaignChannel


class SocialService:
    """Facade hiding provider-specific message sending APIs."""

    def send_message(self, channel: CampaignChannel, destination: str, content: str) -> None:
        """Simulate sending a message through the configured channel."""

        # Real implementation would call external SDKs; we log/print for demo.
        print(f"Sending via {channel.channel_type} to {destination}: {content}")

    def send_email(self, destination: str, subject: str, body: str) -> None:
        """Simulate sending an email."""

        print(f"Email to {destination}: {subject} -> {body}")


def get_social_service() -> SocialService:
    """Dependency provider used by workers or services."""

    return SocialService()
