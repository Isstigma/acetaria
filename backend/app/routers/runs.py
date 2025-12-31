from fastapi import APIRouter, Depends, Query
from datetime import datetime, timezone
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.core.db import get_db
from app.schemas.common import Page
from app.schemas.runs import LatestRunCardOut, MetricOut
from app.schemas.media import VideoOut

router = APIRouter(tags=["runs"])

DEFAULT_VIDEO = VideoOut(
    platform="youtube",
    url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    title="Placeholder video",
    durationMs=0,
    thumbnailUrl="https://cdn.acetaria.example/thumbnails/placeholder.jpg",
)


@router.get("/runs/latest", response_model=Page[LatestRunCardOut])
async def latest_runs(
    limit: int = Query(default=10, ge=1, le=50),
    db: AsyncIOMotorDatabase = Depends(get_db),
):
    total = await db.runs.count_documents({})
    cursor = db.runs.find({}).sort("publishedAt", -1).limit(limit)

    items = []
    async for doc in cursor:
        metric_doc = doc.get("metric") or {"type": "cycles", "cycles": 999}
        metric = MetricOut(
            type=metric_doc["type"],
            cycles=metric_doc.get("cycles"),
            timeMs=metric_doc.get("timeMs"),
        )
        video_raw = doc.get("video")
        video = DEFAULT_VIDEO if not isinstance(video_raw, dict) else VideoOut(**video_raw)

        items.append(
            LatestRunCardOut(
                runId=doc.get("runId", "run_unknown"),
                gameSlug=doc.get("gameSlug", "hsr"),
                gameName=doc.get("gameName", "Honkai: Star Rail"),
                modeSlug=doc.get("modeSlug", "memory-of-chaos"),
                modeName=doc.get("modeName", "Memory of Chaos"),
                title=doc.get("title", "Untitled Run"),
                place=int(doc.get("place", 999)),
                metric=metric,
                playerName=doc.get("playerName", "Unknown"),
                publishedAt=doc.get("publishedAt") or datetime.now(timezone.utc),
                video=video,
            )
        )

    return Page(items=items, page=1, pageSize=limit, total=total)
