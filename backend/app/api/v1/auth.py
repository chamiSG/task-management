"""Authentication endpoints (JWT-based)."""

from __future__ import annotations

from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from app.config import Settings, get_settings
from app.security import User, authenticate_demo_user, create_access_token


router = APIRouter(prefix="/auth", tags=["auth"])


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


@router.post("/login", response_model=TokenResponse, summary="Obtain JWT access token")
async def login(
    payload: LoginRequest,
    settings: Settings = Depends(get_settings),
) -> TokenResponse:
    """
    Authenticate with username and password and receive a JWT access token.
    """
    user: User | None = authenticate_demo_user(payload.username, payload.password, settings)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=settings.access_token_expires_minutes)
    token = create_access_token(
        data={"sub": user.username},
        settings=settings,
        expires_delta=access_token_expires,
    )
    return TokenResponse(access_token=token)

