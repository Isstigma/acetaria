import json
from typing import Annotated, Optional
from fastapi import APIRouter, Body, Depends, Path, Query
from datetime import datetime, timezone
import httpx
import requests
import aiohttp

from sqlmodel import Session, Session, select
from sqlalchemy.orm import joinedload, noload, selectinload
from app.core.db import get_session
from app.schemas.common import Page
from app.schemas.runs import LatestRunCardOut, MetricOut, RunIn, RunOut
from app.schemas.media import VideoOut
from app.core.models import Char, Cost, Run, RunCost, Team, Unit
from app.core.enums import ElementEnum, PathEnum, ResultFlags, RunStatusEnum
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(tags=["runs"])

WEBHOOK_URL = 'https://discord.com/api/webhooks/1462751270883426365/esb5S9OS9m7adRtfaf2FI6xUHk5c7pxx6vHK7DrHK8T3gvrAXsaT5XoUpUt1JctpVKGF'

DEFAULT_VIDEO = VideoOut(
    platform="youtube",
    url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    title="Placeholder video",
    durationMs=0,
    thumbnailUrl="https://cdn.acetaria.example/thumbnails/placeholder.jpg",
)

LTD_CHARS = [1415,1321,1112,1014,1005,1015,1006,1306,1204,1305,1220,1307,1205,1310,1225,1221,1308,1313,1212,1102,1208,1203,1222,1403,1412,1303,1217,1314,1317,1410,1404,1218,1402,1302,1304,1401,1405,1315,1309,1414,1406,1409,1408,1413,1407,1213,1501,1502,1504]
STD_CHARS = [1107,1004,1104,1003,1101,1209,1211] 

LTD_LCS = [23051,23050,23024,23030,23029,23008,23001,23007,23006,23015,23020,23010,23021,23031,23026,23014,23023,23017,23019,23022,23027,23032,23011,23028,23025,23009,23018,23045,23048,23040,23044,23043,23041,23038,23046,23037,23035,23042,23047,23036,23034, 23049, 23052, 23039, 23016, 23056, 23033, 22006, 23054, 23053] 
STD_LCS = [23003,23004,23005,23000,23002,23012,23013] 

def getUnitCost(unit: Unit) -> tuple[int, int]:
    ltd_cost = 0
    std_cost = 0
    
    if unit.char_id in LTD_CHARS:
      ltd_cost += (unit.char_eidolon + 1)
    elif unit.char_id in STD_CHARS:
      std_cost += (unit.char_eidolon + 1)
        
    if unit.lc_id in LTD_LCS:
      ltd_cost += unit.lc_superimposition
    elif unit.lc_id in STD_LCS:
      std_cost += unit.lc_superimposition

    return (ltd_cost, std_cost)
 

@router.get("/runs-status")
async def get_runs_status(
    session: AsyncSession = Depends(get_session),
    refs : Annotated[list[str] | None, Query()] = None
):
    runs  = (await session.execute(select(Run)
      .options(
        noload(Run.team)
        .noload(Team.units)
        .noload(Unit.char)
        ,noload(Run.run_costs)
        ,noload(Run.game_mode_entry)
        )
        .where(Run.submission_ref.in_(refs))
    )).scalars().all()

    result = {run.submission_ref: {"moderator": run.reviewed_by, "timestamp": run.reviewed_at, "status": run.status.name} 
              for run 
              in runs}
    return result

@router.get("/runs/{stage_id}", response_model=list[RunOut])
@router.get("/runs", response_model=list[RunOut])
async def runs_by_stage_id(stage_id: Optional[int]  = None,                                                 session: AsyncSession = Depends(get_session),
                        paths: Annotated[list[PathEnum] | None, Query()] = None,
                        elements: Annotated[list[ElementEnum] | None, Query()] = None,
                        chars: Annotated[list[int] | None, Query()] = None,
                        id : Annotated[str | None, Query()] = None,
                        author_name : Annotated[str | None, Query()] = None,
                        include_pending: Annotated[bool, Query()] = False
    ):
    query  = (select(Run)
      .options(
        joinedload(Run.team)
        .joinedload(Team.units)
        .joinedload(Unit.char)
        ,joinedload(Run.run_costs)
        ,noload(Run.game_mode_entry)
        )
    )

    if not include_pending:
        query = query.where(Run.status == RunStatusEnum.Approved)

    if stage_id is not None:      
      query = query.where(Run.game_mode_entry_id == stage_id)

    if id is not None:
      query = query.where(Run.id == id)

    if author_name is not None:
      query = query.where(Run.author.ilike(f"%{author_name}%"))

    if chars is not None:
        query = query.where(Char.id.in_(chars))
    else: 
        if paths is not None:
            query = query.where(Char.path.in_(paths))
        if elements is not None:
            query = query.where(Char.element.in_(elements))
    # print(query)
    runs = (await session.execute(query)).unique().scalars().all()

    return runs

@router.post("/runs")
async def submit_run(
  session: AsyncSession = Depends(get_session),
  request: RunIn = Body()
):
  #todo blacklist check + author + name retrieval
          # # === Deep Blacklist Check ===
        # video_url = data.get('video_url', '')
        # if video_url:
        #     detected_authors = await get_video_author(video_url)
        #     if detected_authors:
        #         print(f"Deep Check: Found authors {detected_authors} for {video_url}")
        #         blacklist_data = load_blacklist()
                
        #         # Check against 'authors' list
        #         for blocked in blacklist_data.get('authors', []):
        #             blocked_name = blocked['name'] if isinstance(blocked, dict) else blocked
                    
        #             # Exact match check
        #             if blocked_name.lower() in detected_authors:
        #                  print(f"❌ Rejected submission from blacklisted channel: {blocked_name}")
        #                  return web.Response(text=f"Blocked: The channel/author '{blocked_name}' is blacklisted.", status=403)

  units = []
  std_cost = 0
  ltd_cost = 0
  std_cost_entity = (await session.execute(select(Cost).where(Cost.name.ilike("%Standard%")))).scalar_one()
  ltd_cost_entity = (await session.execute(select(Cost).where(Cost.name.ilike("%Limited%")))).scalar_one()
  print(std_cost_entity, ltd_cost_entity)
  for i, unit in enumerate(request.units):
    unit = Unit(char_id = unit.char_id, char_eidolon=unit.char_eidolon, 
                lc_id=unit.lc_id, lc_superimposition=unit.lc_superimposition, is_main=(i==0))
    existingUnit = (await session.execute(select(Unit).filter_by(
       char_id=unit.char_id, 
       char_eidolon=unit.char_eidolon,
       lc_id=unit.lc_id, 
       lc_superimposition=unit.lc_superimposition,
       is_main=unit.is_main))).scalar_one_or_none()
    if existingUnit:
      unit = existingUnit
    units.append(unit)
    unit_std_cost, unit_ltd_cost = getUnitCost(unit)
    std_cost += unit_std_cost
    ltd_cost += unit_ltd_cost


  print(units)
  run_costs : list[RunCost] = []
  print(std_cost_entity, ltd_cost_entity)
  run_costs.append(RunCost(cost=std_cost_entity, cost_id=std_cost_entity.id, value=std_cost))
  run_costs.append(RunCost(cost=ltd_cost_entity, cost_id=ltd_cost_entity.id, value=ltd_cost))
  
  team = Team(name=request.name)
  session.add(team)
  session.add_all(units)
  await session.commit()
  await session.refresh(team)
  for unit in units:
    await session.refresh(unit)#todo fix refresh all units if possible, currently it only works because of the way the session is configured with expire_on_commit=False, but it is still not ideal
  team.units = units

  run = Run(
    team=team,
    game_mode_entry_id=request.stage_id,
    primary_score=request.primary_score,
    secondary_score=request.secondary_score,
    flags=request.flags if request.flags != ResultFlags(0) else None, 
    author=request.author,
    link=request.link,
    name=request.name,
    status=RunStatusEnum.Pending, 
    submitted_by=request.submitted_by,
    run_costs=run_costs,
    submission_ref=request.submission_ref
  )


  session.add(run)
  await session.commit()
  await session.refresh(run)

  session.add_all(run_costs)
  await session.commit()
  
  try:
      # print(request)
      with aiohttp.MultipartWriter('form-data') as mp:
          request_content = json.dumps({"embeds": [json.loads(request.embed_discord)], "content": str(run.id)})
          print(request_content)
          part = mp.append(request_content)
          part.set_content_disposition('form-data', name='payload_json')
          
          async with aiohttp.ClientSession() as session:
              async with session.post(WEBHOOK_URL, data=mp) as resp:
                  if resp.ok:
                      pass
                  else:
                      print(await resp.json())
  except Exception as e:
      print(f"Error in /submit: {e}")

  return {"run_id": run.id}

@router.patch("/runs/reject/{submissionId}/{rejectedBy}")
async def reject_submission(
  submissionId: str, 
  rejectedBy: str,
  session: AsyncSession = Depends(get_session)
):
  run = (await session.execute(select(Run).where(Run.id == submissionId))).scalar()
  run.status = RunStatusEnum.Rejected
  run.reviewed_by = rejectedBy
  run.reviewed_at = datetime.utcnow()
  session.commit()

@router.patch("/runs/approve/{submissionId}/{approvedBy}")
async def approve_submission(
  submissionId: str,
  approvedBy: str,
  session: AsyncSession = Depends(get_session)
):
  run = (await session.execute(select(Run).where(Run.id == submissionId))).scalar()
  run.status = RunStatusEnum.Approved
  run.reviewed_by = approvedBy
  run.reviewed_at = datetime.now()
  session.commit()
