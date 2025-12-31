from fastapi import APIRouter, Query
from app.schemas.common import Page
from pydantic import BaseModel, Field
from typing import Literal, Optional, List
from datetime import datetime, timezone


router = APIRouter(tags=["meta"])


class LanguageOut(BaseModel):
    code: str
    name: str


class NavItemOut(BaseModel):
    id: str
    title: str
    summary: str
    createdAt: datetime


class SearchResultOut(BaseModel):
    type: Literal["run", "leaderboard_entry", "guide", "resource", "forum_thread", "challenge"]
    id: str
    title: str
    snippet: str
    url: str


class AuthOut(BaseModel):
    ok: bool = True
    message: str
    token: str = "dummy-token"
    role: Literal["admin", "moderator", "user"] = "user"


class FilterOptionOut(BaseModel):
    key: str
    label: str
    type: Literal["toggle", "select", "text"]
    values: Optional[List[str]] = None


class StatsOut(BaseModel):
    gameSlug: str
    modeSlug: Optional[str] = None
    totalRuns: int = Field(ge=0)
    totalLeaderboardEntries: int = Field(ge=0)
    totalTeamEntries: int = Field(ge=0)


@router.get("/meta/languages", response_model=Page[LanguageOut])
async def list_languages(page: int = 1, pageSize: int = 50):
    # Languages in your screenshot + Ukrainian (remove if undesired).
    items = [
        LanguageOut(code="en", name="English"),
        LanguageOut(code="id", name="Bahasa Indonesia"),
        LanguageOut(code="ja", name="日本語"),
        LanguageOut(code="ko", name="한국어"),
        LanguageOut(code="ru", name="Русский"),
        LanguageOut(code="vi", name="Tiếng Việt"),
        LanguageOut(code="zh-CN", name="简体中文"),
        LanguageOut(code="zh-TW", name="繁體中文"),
        LanguageOut(code="uk", name="Українська"),
    ]
    total = len(items)
    start = (page - 1) * pageSize
    end = start + pageSize
    return Page(items=items[start:end], page=page, pageSize=pageSize, total=total)


@router.get("/search", response_model=Page[SearchResultOut])
async def search(q: str = Query(default=""), page: int = 1, pageSize: int = 20):
    base = [
        SearchResultOut(
            type="run",
            id="run_featured_001",
            title="HSR • Memory of Chaos • 0-Cycle",
            snippet="Seeded run result (dummy search response).",
            url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        ),
        SearchResultOut(
            type="guide",
            id="guide_001",
            title="MoC Routing Guide (placeholder)",
            snippet="Seeded guide (dummy search response).",
            url="/hsr",
        ),
    ]
    items = [x for x in base if q.lower() in x.title.lower()] if q else base
    total = len(items)
    start = (page - 1) * pageSize
    end = start + pageSize
    return Page(items=items[start:end], page=page, pageSize=pageSize, total=total)


@router.get("/challenges", response_model=Page[NavItemOut])
async def list_challenges(page: int = 1, pageSize: int = 20):
    now = datetime.now(timezone.utc)
    items = [
        NavItemOut(id="ch_001", title="0-Cycle Challenge Week", summary="Placeholder challenge list item.", createdAt=now),
        NavItemOut(id="ch_002", title="Low Investment Showcase", summary="Placeholder challenge list item.", createdAt=now),
    ]
    total = len(items)
    start = (page - 1) * pageSize
    end = start + pageSize
    return Page(items=items[start:end], page=page, pageSize=pageSize, total=total)


@router.get("/forums", response_model=Page[NavItemOut])
async def list_forums(page: int = 1, pageSize: int = 20):
    now = datetime.now(timezone.utc)
    items = [
        NavItemOut(id="f_001", title="HSR General", summary="Placeholder forum board.", createdAt=now),
        NavItemOut(id="f_002", title="Runs & Routing", summary="Placeholder forum board.", createdAt=now),
    ]
    total = len(items)
    start = (page - 1) * pageSize
    end = start + pageSize
    return Page(items=items[start:end], page=page, pageSize=pageSize, total=total)


@router.get("/help", response_model=Page[NavItemOut])
async def list_help(page: int = 1, pageSize: int = 20):
    now = datetime.now(timezone.utc)
    items = [
        NavItemOut(id="h_001", title="Getting Started", summary="How Acetaria works (placeholder).", createdAt=now),
        NavItemOut(id="h_002", title="Submission Rules", summary="Run/video rules (placeholder).", createdAt=now),
    ]
    total = len(items)
    start = (page - 1) * pageSize
    end = start + pageSize
    return Page(items=items[start:end], page=page, pageSize=pageSize, total=total)


# Auth placeholders (NOT real auth)
class LoginIn(BaseModel):
    email: str
    password: str


class SignupIn(BaseModel):
    email: str
    password: str
    displayName: str


@router.post("/auth/login", response_model=AuthOut)
async def login(_: LoginIn):
    return AuthOut(ok=True, message="Login placeholder (auth not implemented).", role="user")


@router.post("/auth/signup", response_model=AuthOut)
async def signup(_: SignupIn):
    return AuthOut(ok=True, message="Signup placeholder (auth not implemented).", role="user")


# Game tabs (placeholders)
@router.get("/games/{gameSlug}/news", response_model=Page[NavItemOut])
async def game_news(gameSlug: str, page: int = 1, pageSize: int = 20):
    now = datetime.now(timezone.utc)
    items = [NavItemOut(id=f"n_{gameSlug}_001", title="Patch Notes (placeholder)", summary="Seeded news item.", createdAt=now)]
    return Page(items=items, page=page, pageSize=pageSize, total=len(items))


@router.get("/games/{gameSlug}/guides", response_model=Page[NavItemOut])
async def game_guides(gameSlug: str, page: int = 1, pageSize: int = 20):
    now = datetime.now(timezone.utc)
    items = [NavItemOut(id=f"g_{gameSlug}_001", title="MoC Routing Guide (placeholder)", summary="Seeded guide item.", createdAt=now)]
    return Page(items=items, page=page, pageSize=pageSize, total=len(items))


@router.get("/games/{gameSlug}/resources", response_model=Page[NavItemOut])
async def game_resources(gameSlug: str, page: int = 1, pageSize: int = 20):
    now = datetime.now(timezone.utc)
    items = [NavItemOut(id=f"r_{gameSlug}_001", title="Useful Links (placeholder)", summary="Seeded resources item.", createdAt=now)]
    return Page(items=items, page=page, pageSize=pageSize, total=len(items))


@router.get("/games/{gameSlug}/streams", response_model=Page[NavItemOut])
async def game_streams(gameSlug: str, page: int = 1, pageSize: int = 20):
    now = datetime.now(timezone.utc)
    items = [NavItemOut(id=f"s_{gameSlug}_001", title="Featured Stream (placeholder)", summary="Seeded streams item.", createdAt=now)]
    return Page(items=items, page=page, pageSize=pageSize, total=len(items))


@router.get("/games/{gameSlug}/stats", response_model=StatsOut)
async def game_stats(gameSlug: str, mode: Optional[str] = None):
    return StatsOut(gameSlug=gameSlug, modeSlug=mode, totalRuns=1, totalLeaderboardEntries=48, totalTeamEntries=3)


@router.get("/games/{gameSlug}/leaderboards/filters", response_model=Page[FilterOptionOut])
async def leaderboard_filters(gameSlug: str, mode: str, page: int = 1, pageSize: int = 50):
    items = [
        FilterOptionOut(key="filter", label="Filter", type="select", values=["All", "Verified", "New"]),
        FilterOptionOut(key="zeroCycle", label="0-Cycle", type="toggle"),
        FilterOptionOut(key="fullStars", label="Full stars", type="toggle"),
    ]
    return Page(items=items, page=page, pageSize=pageSize, total=len(items))


class SubmitRunIn(BaseModel):
    gameSlug: str
    modeSlug: str
    title: str
    videoUrl: str


@router.post("/runs/submit")
async def submit_run(_: SubmitRunIn):
    return {"ok": True, "message": "Submit placeholder (no persistence in MVP)."}
