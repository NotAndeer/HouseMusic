"""Social account management endpoints."""

from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_active_user
from app.db.session import get_db
from app.models.social_account import SocialAccount
from app.models.user import User
from app.schemas.social_account import SocialAccountOut

router = APIRouter()


@router.get("/social-accounts", response_model=list[SocialAccountOut])
def list_social_accounts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> list[SocialAccount]:
    return db.query(SocialAccount).filter(SocialAccount.user_id == current_user.id).all()


@router.delete("/social-accounts/{account_id}", status_code=status.HTTP_204_NO_CONTENT)
def disconnect_social_account(
    account_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> None:
    account = db.query(SocialAccount).filter(
        SocialAccount.id == account_id,
        SocialAccount.user_id == current_user.id
    ).first()
    if not account:
        raise HTTPException(status_code=404, detail="Social account not found")
    db.delete(account)
    db.commit()
    return