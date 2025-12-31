from fastapi import APIRouter, Depends, HTTPException, Query
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.core.db import get_db
from app.schemas.common import Page
from app.schemas.leaderboards import (
    LeaderboardEntryOut,
    TeamEntryOut,
    CharacterOut,
    PlayerOut,
    TeamMemberPortraitOut,
)
from app.schemas.media import VideoOut
from app.schemas.runs import MetricOut

router = APIRouter(tags=["leaderboards"])

DEFAULT_VIDEO = VideoOut(
    platform="youtube",
    url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    title="Placeholder video",
    durationMs=0,
    thumbnailUrl="https://cdn.acetaria.example/thumbnails/placeholder.jpg",
)

PAD_PORTRAIT_URL = "https://cdn.acetaria.example/hsr/portraits/pad.png"


def _safe_player_display(doc: dict) -> str:
    p = doc.get("player")
    if isinstance(p, dict):
        return p.get("displayName") or "Unknown"
    return "Unknown"


def _pad_team(team_raw) -> list[TeamMemberPortraitOut]:
    out: list[TeamMemberPortraitOut] = []
    if isinstance(team_raw, list):
        for m in team_raw[:4]:
            if isinstance(m, dict) and "id" in m and "portraitUrl" in m:
                out.append(TeamMemberPortraitOut(**m))

    while len(out) < 4:
        out.append(TeamMemberPortraitOut(id=f"pad_{len(out)}", portraitUrl=PAD_PORTRAIT_URL))
    return out


@router.get("/games/{gameSlug}/leaderboards", response_model=Page[LeaderboardEntryOut])
async def get_leaderboards(
    gameSlug: str,
    mode: str = Query(..., description="modeSlug"),
    page: int = 1,
    pageSize: int = 50,
    db: AsyncIOMotorDatabase = Depends(get_db),
):
    game = await db.games.find_one({"slug": gameSlug})
    if not game:
        raise HTTPException(404, "Game not found")

    mode_doc = await db.modes.find_one({"gameSlug": gameSlug, "modeSlug": mode})
    if not mode_doc:
        raise HTTPException(404, "Mode not found")

    play_metric_type = mode_doc["playMetricType"]
    sort_field = "cycles" if play_metric_type == "cycles" else "timeMs"

    q = {"gameSlug": gameSlug, "modeSlug": mode}
    total = await db.leaderboard_entries.count_documents(q)
    cursor = (
        db.leaderboard_entries.find(q)
        .sort([(sort_field, 1), ("limStd", 1), ("entryId", 1)])
        .skip((page - 1) * pageSize)
        .limit(pageSize)
    )

    items: list[LeaderboardEntryOut] = []
    async for doc in cursor:
        metric = MetricOut(
            type=play_metric_type,
            cycles=doc.get("cycles") if play_metric_type == "cycles" else None,
            timeMs=doc.get("timeMs") if play_metric_type == "time" else None,
        )
        items.append(
            LeaderboardEntryOut(
                entryId=doc.get("entryId", "entry_missing"),
                character=CharacterOut(**doc["character"]),
                limStd=int(doc.get("limStd", 0)),
                metric=metric,
                player=PlayerOut(displayName=_safe_player_display(doc)),
                rank=None,
            )
        )

    return Page(items=items, page=page, pageSize=pageSize, total=total)


@router.get("/leaderboard-entries/{entryId}/teams", response_model=Page[TeamEntryOut])
async def get_entry_teams(
    entryId: str,
    page: int = 1,
    pageSize: int = 20,
    db: AsyncIOMotorDatabase = Depends(get_db),
):
    entry = await db.leaderboard_entries.find_one({"entryId": entryId})
    if not entry:
        raise HTTPException(404, "Leaderboard entry not found")

    mode_doc = await db.modes.find_one({"gameSlug": entry["gameSlug"], "modeSlug": entry["modeSlug"]})
    if not mode_doc:
        raise HTTPException(500, "Mode missing for entry")

    play_metric_type = mode_doc["playMetricType"]
    sort_field = "cycles" if play_metric_type == "cycles" else "timeMs"

    q = {"entryId": entryId}
    total = await db.team_entries.count_documents(q)
    cursor = (
        db.team_entries.find(q)
        .sort([(sort_field, 1), ("limStd", 1), ("teamEntryId", 1)])
        .skip((page - 1) * pageSize)
        .limit(pageSize)
    )

    items: list[TeamEntryOut] = []
    async for doc in cursor:
        metric = MetricOut(
            type=play_metric_type,
            cycles=doc.get("cycles") if play_metric_type == "cycles" else None,
            timeMs=doc.get("timeMs") if play_metric_type == "time" else None,
        )

        video_raw = doc.get("video")
        video = DEFAULT_VIDEO if not isinstance(video_raw, dict) else VideoOut(**video_raw)

        items.append(
            TeamEntryOut(
                teamEntryId=doc.get("teamEntryId", "teamEntry_missing"),
                team=_pad_team(doc.get("team")),
                limStd=int(doc.get("limStd", 0)),
                metric=metric,
                player=PlayerOut(displayName=_safe_player_display(doc)),
                video=video,
            )
        )

    return Page(items=items, page=page, pageSize=pageSize, total=total)
