"""User management endpoints."""

from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_active_user, get_current_active_superuser
from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserOut, UserUpdate

router = APIRouter()


@router.get("/users/me", response_model=UserOut)
def read_current_user(current_user: User = Depends(get_current_active_user)) -> User:
    return current_user


@router.get("/users", response_model=list[UserOut])
def list_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser),
) -> list[User]:
    return db.query(User).offset(skip).limit(limit).all()


@router.patch("/users/{user_id}", response_model=UserOut)
def update_user(
    user_id: UUID,
    update_data: UserUpdate,  # ← ¡CORREGIDO AQUÍ!
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> User:
    if not current_user.is_superuser and current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    update_dict = update_data.model_dump(exclude_unset=True)
    if not current_user.is_superuser:
        update_dict.pop("is_superuser", None)
        update_dict.pop("is_active", None)

    for field, value in update_dict.items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)
    return user