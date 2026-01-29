from typing import Annotated
from fastapi import APIRouter, Body, Depends, Path, Query
from datetime import datetime, timezone

from sqlmodel import Session, Session, select
from app.core.db import get_session
from app.schemas.common import Page
from app.schemas.runs import LatestRunCardOut, MetricOut, RunIn, RunOut
from app.schemas.media import VideoOut
from app.core.models import Char, Run, Team, Unit
from app.core.enums import ElementEnum, PathEnum, RunStatusEnum

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
    # db: AsyncIOMotorDatabase = Depends(get_db),
):
    # total = await db.runs.count_documents({})
    # cursor = db.runs.find({}).sort("publishedAt", -1).limit(limit)

    items = []
    # async for doc in cursor:
    #     metric_doc = doc.get("metric") or {"type": "cycles", "cycles": 999}
    #     metric = MetricOut(
    #         type=metric_doc["type"],
    #         cycles=metric_doc.get("cycles"),
    #         timeMs=metric_doc.get("timeMs"),
    #     )
    #     video_raw = doc.get("video")
    #     video = DEFAULT_VIDEO if not isinstance(video_raw, dict) else VideoOut(**video_raw)

    #     items.append(
    #         LatestRunCardOut(
    #             runId=doc.get("runId", "run_unknown"),
    #             gameSlug=doc.get("gameSlug", "hsr"),
    #             gameName=doc.get("gameName", "Honkai: Star Rail"),
    #             modeSlug=doc.get("modeSlug", "memory-of-chaos"),
    #             modeName=doc.get("modeName", "Memory of Chaos"),
    #             title=doc.get("title", "Untitled Run"),
    #             place=int(doc.get("place", 999)),
    #             metric=metric,
    #             playerName=doc.get("playerName", "Unknown"),
    #             publishedAt=doc.get("publishedAt") or datetime.now(timezone.utc),
    #             video=video,
    #         )
    #     )

    return Page(items=items, page=1, pageSize=limit, total=0)#todo upd total

@router.get("/runs/{stage_id}", response_model=list[RunOut])
async def runs_by_entry(stage_id: int,                         
                        session: Session = Depends(get_session),
                        paths: Annotated[list[PathEnum] | None, Query()] = None,
                        elements: Annotated[list[ElementEnum] | None, Query()] = None,
                        chars: Annotated[list[int] | None, Query()] = None
    ):
    query  = (select(Run)
        .join(Team)
        .join(Unit, Team.units)
        .join(Char)
        .where(Run.game_mode_entry_id == stage_id)
    )

    if chars is not None:
        query = query.where(Char.id.in_(chars))
    else: 
        if paths is not None:
            query = query.where(Char.path.in_(paths))
        if elements is not None:
            query = query.where(Char.element.in_(elements))

    runs = session.exec(query).all()

    return runs

@router.post("/runs")
async def submit_run(
  session: Session = Depends(get_session),
  request: RunIn = Body()
):
  units = []
  for unit in request.units:
    unit = Unit(char_id = unit.char_id, char_eidolon=unit.char_eidolon, 
                lc_id=unit.lc_id, lc_superimposition=unit.lc_superimposition)
    existingUnit = session.query(Unit).filter_by(
       char_id=unit.char_id, 
       char_eidolon=unit.char_eidolon,
       lc_id=unit.lc_id, 
       lc_superimposition=unit.lc_superimposition).first()
    if existingUnit:
      unit = existingUnit
    print('-------checking existing unit-------')
    print(existingUnit)
    print('------------------------------------')
    units.append(unit)
  team = Team(name=request.name, units=units)
  run = Run(
    team=team,
    game_mode_entry_id=request.stage_id,
    primary_score=request.primary_score,
    secondary_score=request.secondary_score,
    flags=request.flags,
    author=request.author,
    link=request.link,
    name=request.name,
    status=RunStatusEnum.Pending,
    submitted_by=request.submitted_by,
  )
  session.add(run)
  session.commit()
  session.refresh(run)
  return {"run_id": run.id}

@router.delete("/runs/reject/{submissionId}/{rejecteddBy}")
async def reject_submission(
  submissionId: str, 
  rejectedBy: str,
  session: Session = Depends(get_session)
):
  pass

@router.patch("/runs/approve/{submissionId}/{approvedBy}")
async def approve_submission(
  submissionId: str,
  session: Session = Depends(get_session)
):
  pass