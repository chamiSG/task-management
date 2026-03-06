from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Any, Optional

import bcrypt
from jose import JWTError, jwt
from pydantic import BaseModel
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.config import Settings, get_settings


http_bearer = HTTPBearer(auto_error=True)


class User(BaseModel):
    username: str


class TokenData(BaseModel):
    sub: str
    exp: datetime


def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return bcrypt.checkpw(
            plain_password.encode("utf-8"),
            hashed_password.encode("utf-8"),
        )
    except (ValueError, TypeError):
        return False


def get_password_hash(password: str) -> str:
    return bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt(rounds=12),
    ).decode("utf-8")


def create_access_token(
    data: dict[str, Any],
    *,
    settings: Settings,
    expires_delta: Optional[timedelta] = None,
) -> str:
    to_encode = data.copy()
    expire = datetime.now(UTC) + (
        expires_delta
        if expires_delta is not None
        else timedelta(minutes=settings.access_token_expires_minutes)
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )
    return encoded_jwt


def authenticate_demo_user(username: str, password: str, settings: Settings) -> Optional[User]:
    """
    Simple demo authentication that checks credentials against values
    provided via configuration (environment variables).
    """
    if username != settings.demo_username:
        return None

    demo_hashed = get_password_hash(settings.demo_password)
    if not verify_password(password, demo_hashed):
        return None

    return User(username=username)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
    settings: Settings = Depends(get_settings),
) -> User:
    """
    Dependency that validates a JWT bearer token and returns the current user.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = credentials.credentials
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm],
        )
        sub = payload.get("sub")
        exp = payload.get("exp")
        if sub is None or exp is None:
            raise credentials_exception

        token_data = TokenData(sub=sub, exp=datetime.fromtimestamp(exp, tz=UTC))
    except JWTError:
        raise credentials_exception

    return User(username=token_data.sub)

