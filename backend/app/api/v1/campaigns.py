"""Campaign endpoints for CRUD-lite operations."""

from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.campaign import CampaignCreate, CampaignOut, CampaignUpdate
from app.services.campaign_service import CampaignService, get_campaign_service

router = APIRouter()


@router.get("/campaigns", response_model=list[CampaignOut])
def list_campaigns(
    service: CampaignService = Depends(get_campaign_service),
) -> list[CampaignOut]:
    """List all campaigns for dashboard usage."""
    campaigns = service.get_all_campaigns()
    return [CampaignOut.model_validate(c) for c in campaigns]


@router.post("/campaigns", response_model=CampaignOut, status_code=status.HTTP_201_CREATED)
def create_campaign(
    payload: CampaignCreate,
    service: CampaignService = Depends(get_campaign_service),
) -> CampaignOut:
    """Create a campaign and its associated channels."""
    campaign = service.create_campaign(
        name=payload.name,
        description=payload.description,
        channels=[c.model_dump() for c in payload.channels],
    )
    return CampaignOut.model_validate(campaign)


@router.put("/campaigns/{campaign_id}", response_model=CampaignOut)
def update_campaign(
    campaign_id: UUID,
    payload: CampaignUpdate,
    service: CampaignService = Depends(get_campaign_service),
) -> CampaignOut:
    """Update campaign metadata."""
    try:
        campaign = service.update_campaign(
            campaign_id=campaign_id,
            update_data=payload.model_dump(exclude_unset=True),
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    return CampaignOut.model_validate(campaign)