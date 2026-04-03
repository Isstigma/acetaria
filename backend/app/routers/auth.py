from __future__ import annotations

from urllib.parse import urlencode

import httpx
from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from fastapi.responses import JSONResponse, RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.core.auth import (
    OAUTH_STATE_COOKIE_NAME,
    SESSION_COOKIE_NAME,
    build_avatar_url,
    create_oauth_state,
    create_session_token,
    get_current_user,
    validate_oauth_state,
)
from app.core.config import settings
from app.core.db import get_session
from app.core.models import User

router = APIRouter(prefix="/auth", tags=["auth"])

DISCORD_AUTHORIZE_URL = "https://discord.com/oauth2/authorize"
DISCORD_TOKEN_URL = "https://discord.com/api/oauth2/token"
DISCORD_USER_URL = "https://discord.com/api/users/@me"


@router.get("/discord/login")
async def discord_login() -> RedirectResponse:
    if not settings.discord_client_id or not settings.discord_client_secret:
        raise HTTPException(status_code=500, detail="Discord OAuth is not configured")

    state = create_oauth_state()
    params = {
        "response_type": "code",
        "client_id": settings.discord_client_id,
        "scope": settings.discord_oauth_scope,
        "redirect_uri": settings.discord_redirect_uri,
        "state": state,
        "prompt": "consent",
    }
    authorize_url = f"{DISCORD_AUTHORIZE_URL}?{urlencode(params)}"
    response = RedirectResponse(url=authorize_url, status_code=status.HTTP_302_FOUND)
    response.set_cookie(
        key=OAUTH_STATE_COOKIE_NAME,
        value=state,
        httponly=True,
        secure=settings.cookie_secure,
        samesite=settings.cookie_samesite,
        max_age=600,
        path="/",
    )
    return response


@router.get("/discord/callback")
async def discord_callback(
    request: Request,
    code: str | None = Query(default=None),
    state: str | None = Query(default=None),
    error: str | None = Query(default=None),
    session: AsyncSession = Depends(get_session),
):
    if error:
        raise HTTPException(status_code=400, detail=f"Discord OAuth error: {error}")
    if not code or not state:
        raise HTTPException(status_code=400, detail="Missing OAuth code or state")

    cookie_state = request.cookies.get(OAUTH_STATE_COOKIE_NAME) if request else None
    if not cookie_state or cookie_state != state:
        raise HTTPException(status_code=400, detail="Invalid OAuth state")

    try:
        validate_oauth_state(state)
    except Exception as exc:
        raise HTTPException(status_code=400, detail="Expired or invalid OAuth state") from exc

    token_data = {
        "client_id": settings.discord_client_id,
        "client_secret": settings.discord_client_secret,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": settings.discord_redirect_uri,
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    async with httpx.AsyncClient(timeout=20.0) as client:
        token_response = await client.post(DISCORD_TOKEN_URL, data=token_data, headers=headers)
        if token_response.status_code >= 400:
            raise HTTPException(status_code=400, detail=f"Discord token exchange failed: {token_response.text}")

        token_json = token_response.json()
        access_token = token_json.get("access_token")
        token_type = token_json.get("token_type", "Bearer")
        if not access_token:
            raise HTTPException(status_code=400, detail="Discord did not return access_token")

        user_response = await client.get(
            DISCORD_USER_URL,
            headers={"Authorization": f"{token_type} {access_token}"},
        )
        if user_response.status_code >= 400:
            raise HTTPException(status_code=400, detail=f"Discord user lookup failed: {user_response.text}")

        discord_user = user_response.json()

    discord_id = str(discord_user["id"])
    user = (await session.execute(select(User).where(User.discord_id == discord_id))).scalar_one_or_none()

    is_new_user = user is None
    if user is None:
        user = User(
            discord_id=discord_id,
            username=discord_user.get("username") or discord_id,
            global_name=discord_user.get("global_name"),
            avatar=build_avatar_url(discord_id, discord_user.get("avatar")),
            role="admin" if settings.discord_admin_id and discord_id == settings.discord_admin_id else "user",
            is_active=True,
        )
        session.add(user)
        await session.flush()
    else:
        user.username = discord_user.get("username") or user.username
        user.global_name = discord_user.get("global_name")
        user.avatar = build_avatar_url(discord_id, discord_user.get("avatar"))
        user.is_active = True
        session.add(user)

    await session.commit()
    await session.refresh(user)

    redirect_response = RedirectResponse(
        url=settings.frontend_oauth_success_redirect,
        status_code=status.HTTP_302_FOUND,
    )
    redirect_response.set_cookie(
        key=SESSION_COOKIE_NAME,
        value=create_session_token(user),
        httponly=True,
        secure=settings.cookie_secure,
        samesite=settings.cookie_samesite,
        max_age=settings.session_max_age_seconds,
        path="/",
    )
    redirect_response.delete_cookie(OAUTH_STATE_COOKIE_NAME, path="/")
    if is_new_user:
        redirect_response.headers["X-Acetaria-New-User"] = "1"
    return redirect_response


@router.get("/me")
async def auth_me(current_user: User = Depends(get_current_user)) -> dict:
    return {
        "id": current_user.id,
        "discord_id": current_user.discord_id,
        "username": current_user.username,
        "global_name": current_user.global_name,
        "avatar": current_user.avatar,
        "role": current_user.role,
        "is_active": current_user.is_active,
    }


@router.post("/logout")
async def logout() -> JSONResponse:
    response = JSONResponse({"ok": True})
    response.delete_cookie(SESSION_COOKIE_NAME, path="/")
    response.delete_cookie(OAUTH_STATE_COOKIE_NAME, path="/")
    return response
