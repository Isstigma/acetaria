import base64
import hashlib
import hmac
import json
import secrets
import time
from typing import Any

from fastapi import Cookie, Depends, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.core.config import settings
from app.core.db import get_session
from app.core.models import User

ROLE_USER = "user"
ROLE_MODERATOR = "moderator"
ROLE_ADMIN = "admin"
VALID_ROLES = {ROLE_USER, ROLE_MODERATOR, ROLE_ADMIN}


class AuthError(Exception):
    pass


def _b64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("utf-8")


def _b64url_decode(data: str) -> bytes:
    padding = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + padding)


def _sign(value: str) -> str:
    secret = settings.session_secret.encode("utf-8")
    return _b64url_encode(hmac.new(secret, value.encode("utf-8"), hashlib.sha256).digest())


def _encode_payload(payload: dict[str, Any]) -> str:
    raw = json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8")
    encoded = _b64url_encode(raw)
    signature = _sign(encoded)
    return f"{encoded}.{signature}"


def _decode_payload(token: str) -> dict[str, Any]:
    try:
        encoded, signature = token.split(".", 1)
    except ValueError as exc:
        raise AuthError("Invalid token format") from exc

    expected = _sign(encoded)
    if not hmac.compare_digest(signature, expected):
        raise AuthError("Invalid token signature")

    try:
        payload = json.loads(_b64url_decode(encoded))
    except (json.JSONDecodeError, ValueError) as exc:
        raise AuthError("Invalid token payload") from exc

    exp = payload.get("exp")
    if not isinstance(exp, int) or exp < int(time.time()):
        raise AuthError("Token expired")

    return payload


SESSION_COOKIE_NAME = "acetaria_session"
OAUTH_STATE_COOKIE_NAME = "acetaria_oauth_state"


def create_session_token(user: User) -> str:
    now = int(time.time())
    payload = {
        "sub": user.id,
        "role": user.role,
        "iat": now,
        "exp": now + settings.session_max_age_seconds,
        "nonce": secrets.token_urlsafe(8),
    }
    return _encode_payload(payload)


def decode_session_token(token: str) -> dict[str, Any]:
    return _decode_payload(token)


def create_oauth_state() -> str:
    payload = {
        "nonce": secrets.token_urlsafe(24),
        "exp": int(time.time()) + 600,
    }
    return _encode_payload(payload)


def validate_oauth_state(state: str) -> None:
    _decode_payload(state)


async def get_current_user(
    session: AsyncSession = Depends(get_session),
    acetaria_session: str | None = Cookie(default=None, alias=SESSION_COOKIE_NAME),
) -> User:
    if not acetaria_session:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    try:
        payload = decode_session_token(acetaria_session)
    except AuthError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)) from exc

    user_id = payload.get("sub")
    if not isinstance(user_id, str) or not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid session")

    user = (await session.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is inactive")

    return user


async def require_moderator_or_admin(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role not in {ROLE_MODERATOR, ROLE_ADMIN}:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Moderator or admin role required")
    return current_user


async def require_admin(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != ROLE_ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin role required")
    return current_user


def build_avatar_url(discord_user_id: str, avatar_hash: str | None) -> str | None:
    if not avatar_hash:
        return None
    return f"https://cdn.discordapp.com/avatars/{discord_user_id}/{avatar_hash}.png"
