from typing import Annotated
from fastapi import APIRouter, Body, Depends, Path, Query
from datetime import datetime, timezone

from sqlmodel import Session, Session, select
from app.core.db import get_session
from app.schemas.common import Page
from app.schemas.runs import LatestRunCardOut, MetricOut, RunIn, RunOut
from app.schemas.media import VideoOut
from app.core.models import Char, Cost, Run, RunCost, Team, Unit
from app.core.enums import ElementEnum, PathEnum, RunStatusEnum

router = APIRouter(tags=["runs"])

DEFAULT_VIDEO = VideoOut(
    platform="youtube",
    url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    title="Placeholder video",
    durationMs=0,
    thumbnailUrl="https://cdn.acetaria.example/thumbnails/placeholder.jpg",
)

LTD_CHARS = [1415,1321,1112,1014,1005,1015,1006,1306,1204,1305,1220,1307,1205,1310,1225,1221,1308,1313,1212,1102,1208,1203,1222,1403,1412,1303,1217,1314,1317,1410,1404,1218,1402,1302,1304,1401,1405,1315,1309,1414,1406,1409,1408,1413,1407,1213]
STD_CHARS = [1107,1004,1104,1003,1101,1209,1211] 

LTD_LCS = [23051,23050,23024,23030,23029,23008,23001,23007,23006,23015,23020,23010,23021,23031,23026,23014,23023,23017,23019,23022,23027,23032,23011,23028,23025,23009,23018,23045,23048,23040,23044,23043,23041,23038,23046,23037,23035,23042,23047,23036,23034] 
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
 

@router.get("/runs/{stage_id}", response_model=list[RunOut])
async def runs_by_stage_id(stage_id: int,                         
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
  std_cost = 0
  ltd_cost = 0
  std_cost_entity = session.exec(select(Cost).where(Cost.name.ilike("%Standard%"))).first()
  ltd_cost_entity = session.exec(select(Cost).where(Cost.name.ilike("%Limited%"))).first()
  print(std_cost_entity, ltd_cost_entity)
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
    units.append(unit)
    unit_std_cost, unit_ltd_cost = getUnitCost(unit)
    std_cost += unit_std_cost
    ltd_cost += unit_ltd_cost

  run_costs : list[RunCost] = []
  run_costs.append(RunCost(cost=std_cost_entity, cost_id=std_cost_entity.id, value=std_cost))
  run_costs.append(RunCost(cost=ltd_cost_entity, cost_id=ltd_cost_entity.id, value=ltd_cost))
  
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
    run_costs=run_costs
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
  run = session.exec(select(Run).where(Run.id == submissionId)).first()
  run.status = RunStatusEnum.Rejected
  run.reviewed_by = rejectedBy
  session.commit()

@router.patch("/runs/approve/{submissionId}/{approvedBy}")
async def approve_submission(
  submissionId: str,
  approvedBy: str,
  session: Session = Depends(get_session)
):
  run = session.exec(select(Run).where(Run.id == submissionId)).first()
  run.status = RunStatusEnum.Approved
  run.reviewed_by = approvedBy
  session.commit()
