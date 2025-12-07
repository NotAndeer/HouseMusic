"""Campaign orchestration services."""

import uuid
from datetime import datetime

from sqlalchemy.orm import Session

from app.models.campaign import Campaign, CampaignChannel, CampaignStatus
from app.workers.tasks_campaigns import run_campaign


class CampaignService:
    """Encapsulates business rules for campaign lifecycle."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def create_campaign(self, name: str, description: str | None, channels: list[dict]) -> Campaign:
        """Persist a campaign and its channels."""

        campaign = Campaign(name=name, description=description)
        for channel in channels:
            campaign.channels.append(CampaignChannel(**channel))
        self.db.add(campaign)
        self.db.commit()
        self.db.refresh(campaign)
        return campaign

    def schedule_campaign(self, campaign_id: uuid.UUID, scheduled_at: datetime) -> Campaign:
        """Mark a campaign as scheduled and set execution time."""

        campaign = self.db.get(Campaign, campaign_id)
        if not campaign:
            raise ValueError("Campaign not found")
        campaign.status = CampaignStatus.SCHEDULED
        campaign.scheduled_at = scheduled_at
        self.db.commit()
        self.db.refresh(campaign)
        return campaign

    def trigger_campaign(self, campaign_id: uuid.UUID) -> None:
        """Launch campaign asynchronously via Celery."""

        run_campaign.delay(str(campaign_id))


def get_campaign_service(db: Session) -> CampaignService:
    """Dependency helper for routers/workers."""

    return CampaignService(db)
