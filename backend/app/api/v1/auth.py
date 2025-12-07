"""Authentication router handling login and registration."""

import secrets
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import get_db
from app.models.user import User

router = APIRouter()


class TokenResponse(BaseModel):
    """Simple access token response payload."""

    access_token: str
    token_type: str = "bearer"
    expires_at: datetime


class LoginRequest(BaseModel):
    """Credentials used for login."""

    email: EmailStr
    password: str


class RegisterRequest(LoginRequest):
    """Payload for registering a new user."""

    is_superuser: bool = False


def _issue_token(user: User) -> TokenResponse:
    """Create a pseudo JWT for demo purposes.

    For a real implementation a JWT library would sign the payload with
    ``settings.jwt_secret`` and embed claims like subject and expiry. Here we
    return a random token to keep the example self-contained.
    """

    expires_at = datetime.utcnow() + timedelta(minutes=settings.jwt_expiration_minutes)
    token = secrets.token_urlsafe(32)
    return TokenResponse(access_token=token, expires_at=expires_at)


@router.post("/auth/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)) -> TokenResponse:
    """Authenticate a user by email/password and return an access token."""

    user = db.scalar(select(User).where(User.email == payload.email))
    if not user or user.hashed_password != payload.password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User inactive")
    return _issue_token(user)


@router.post("/auth/register", response_model=TokenResponse)
def register(payload: RegisterRequest, db: Session = Depends(get_db)) -> TokenResponse:
    """Create a new user and return an access token.

    Passwords are stored as-is for brevity; in production a secure hash (bcrypt)
    should be used. Registration exists primarily to simplify local testing.
    """

    existing = db.scalar(select(User).where(User.email == payload.email))
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User exists")
    user = User(
        email=payload.email,
        hashed_password=payload.password,
        is_superuser=payload.is_superuser,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return _issue_token(user)
