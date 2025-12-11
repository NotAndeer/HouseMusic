"""Analytics service for marketing dashboards."""

from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from uuid import UUID

from sqlalchemy import func, and_, or_, select
from sqlalchemy.orm import Session

from app.models.campaign import Campaign, CampaignChannel, CampaignStatus, ChannelType
from app.models.contact import Contact
from app.models.interaction_event import InteractionEvent, InteractionEventType


class AnalyticsService:
    """Service for computing marketing metrics from interaction data."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def get_campaign_metrics(
        self, campaign_id: UUID, start_date: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """Compute detailed metrics for a specific campaign."""
        campaign = self.db.get(Campaign, campaign_id)
        if not campaign:
            raise ValueError("Campaign not found")

        base_query = select(InteractionEvent).where(
            InteractionEvent.created_at >= (start_date or campaign.created_at)
        )

        # Total sends: inferred from campaign creation + channel count, or use delivery events
        total_sends = self.db.scalar(
            select(func.count()).select_from(Contact)
        ) * len(campaign.channels)  # Simplified: assumes 1 msg per channel per contact

        # Delivery (if tracked via events)
        deliveries = self.db.scalar(
            base_query.where(InteractionEvent.event_type == InteractionEventType.DELIVERY).count()
        ) or 0

        # Opens (email only)
        opens = self.db.scalar(
            base_query.where(InteractionEvent.event_type == InteractionEventType.EMAIL_OPEN).count()
        ) or 0

        # Clicks (email only)
        clicks = self.db.scalar(
            base_query.where(InteractionEvent.event_type == InteractionEventType.EMAIL_CLICK).count()
        ) or 0

        # Replies (any channel)
        replies = self.db.scalar(
            base_query.where(InteractionEvent.event_type == InteractionEventType.MESSAGE_RECEIVED).count()
        ) or 0

        return {
            "campaign_id": campaign_id,
            "name": campaign.name,
            "status": campaign.status,
            "total_sends": total_sends,
            "deliveries": deliveries,
            "opens": opens,
            "clicks": clicks,
            "replies": replies,
            "open_rate": round(opens / max(deliveries, 1) * 100, 2),
            "click_rate": round(clicks / max(opens, 1) * 100, 2),
            "reply_rate": round(replies / max(deliveries, 1) * 100, 2),
        }

    def get_channel_metrics(
        self, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None
    ) -> List[Dict[str, Any]]:
        """Aggregate metrics by channel type."""
        if not start_date:
            start_date = datetime.utcnow() - timedelta(days=30)
        if not end_date:
            end_date = datetime.utcnow()

        # Get delivery counts by inferred channel (simplified: assume email if email_open/delivery, etc.)
        email_events = self.db.scalar(
            select(func.count()).where(
                and_(
                    InteractionEvent.created_at.between(start_date, end_date),
                    or_(
                        InteractionEvent.event_type == InteractionEventType.EMAIL_OPEN,
                        InteractionEvent.event_type == InteractionEventType.EMAIL_CLICK,
                        InteractionEvent.event_type == InteractionEventType.DELIVERY,
                    )
                )
            )
        ) or 0

        whatsapp_events = self.db.scalar(
            select(func.count()).where(
                and_(
                    InteractionEvent.created_at.between(start_date, end_date),
                    InteractionEvent.event_type == InteractionEventType.MESSAGE_RECEIVED,
                    InteractionEvent.payload_json["channel"].astext == "WHATSAPP"
                )
            )
        ) or 0

        # Note: Instagram/Facebook require parsing payload_json; this is a simplified version
        messenger_events = self.db.scalar(
            select(func.count()).where(
                and_(
                    InteractionEvent.created_at.between(start_date, end_date),
                    InteractionEvent.event_type == InteractionEventType.MESSAGE_RECEIVED,
                    or_(
                        InteractionEvent.payload_json["channel"].astext == "INSTAGRAM",
                        InteractionEvent.payload_json["channel"].astext == "FACEBOOK",
                    )
                )
            )
        ) or 0

        return [
            {"channel": "EMAIL", "total_events": email_events},
            {"channel": "WHATSAPP", "total_events": whatsapp_events},
            {"channel": "INSTAGRAM", "total_events": messenger_events // 2},  # rough split
            {"channel": "FACEBOOK", "total_events": messenger_events // 2},
        ]

    def get_segment_metrics(
        self,
        tag: Optional[str] = None,
        is_opt_in: Optional[bool] = None,
        start_date: Optional[datetime] = None,
    ) -> Dict[str, Any]:
        """Compute engagement metrics for a contact segment."""
        contact_query = select(Contact.id)
        if tag:
            contact_query = contact_query.where(Contact.tags.has_key(tag))  # noqa: W601
        if is_opt_in is not None:
            contact_query = contact_query.where(Contact.is_opt_in == is_opt_in)

        contact_ids = self.db.scalars(contact_query).all()

        if not contact_ids:
            return {
                "segment": {"tag": tag, "is_opt_in": is_opt_in},
                "contact_count": 0,
                "total_interactions": 0,
                "reply_count": 0,
            }

        base_event_query = select(InteractionEvent).where(
            InteractionEvent.contact_id.in_(contact_ids)
        )
        if start_date:
            base_event_query = base_event_query.where(InteractionEvent.created_at >= start_date)

        total_interactions = self.db.scalar(select(func.count()).select_from(base_event_query.subquery()))
        reply_count = self.db.scalar(
            base_event_query.where(InteractionEvent.event_type == InteractionEventType.MESSAGE_RECEIVED).count()
        ) or 0

        return {
            "segment": {
                "tag": tag,
                "is_opt_in": is_opt_in,
                "contact_count": len(contact_ids),
            },
            "total_interactions": total_interactions,
            "reply_count": reply_count,
            "engagement_rate": round(reply_count / max(len(contact_ids), 1) * 100, 2),
        }


def get_analytics_service(db: Session) -> AnalyticsService:
    """Dependency helper for routers."""
    return AnalyticsService(db)