from typing import Annotated

from fastapi import APIRouter, Body, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_session
from app.database.models import Char, Cost, Run, RunCost, Team, Unit
from app.database.enums import ElementEnum, PathEnum, RunStatusEnum
from app.schemas.runs import RunIn, RunOut

router = APIRouter(tags=["runs"])

LTD_CHARS = [1415,1321,1112,1014,1005,1015,1006,1306,1204,1305,1220,1307,1205,1310,1225,1221,1308,1313,1212,1102,1208,1203,1222,1403,1412,1303,1217,1314,1317,1410,1404,1218,1402,1302,1304,1401,1405,1315,1309,1414,1406,1409,1408,1413,1407,1213]
STD_CHARS = [1107,1004,1104,1003,1101,1209,1211] 

LTD_LCS = [23051,23050,23024,23030,23029,23008,23001,23007,23006,23015,23020,23010,23021,23031,23026,23014,23023,23017,23019,23022,23027,23032,23011,23028,23025,23009,23018,23045,23048,23040,23044,23043,23041,23038,23046,23037,23035,23042,23047,23036,23034] 
STD_LCS = [23003,23004,23005,23000,23002,23012,23013] 

def get_unit_cost(unit: Unit) -> tuple[int, int]:
    ltd_cost = std_cost = 0

    if unit.char_id in LTD_CHARS:
        ltd_cost += (unit.char_eidolon + 1)
    elif unit.char_id in STD_CHARS:
        std_cost += (unit.char_eidolon + 1)

    if unit.lc_id in LTD_LCS:
        ltd_cost += unit.lc_superimposition
    elif unit.lc_id in STD_LCS:
        std_cost += unit.lc_superimposition

    return ltd_cost, std_cost


@router.get("/runs/{stage_id}", response_model=list[RunOut])
async def runs_by_stage_id(
    stage_id: int,
    session: AsyncSession = Depends(get_session),
    paths: Annotated[list[PathEnum] | None, Query()] = None,
    elements: Annotated[list[ElementEnum] | None, Query()] = None,
    chars: Annotated[list[int] | None, Query()] = None,
):
    query = select(Run).join(Run.team).join(Team.units).join(Unit.char).where(Run.game_mode_entry_id == stage_id)

    if chars:
        query = query.where(Char.id.in_(chars))
    else:
        if paths:
            query = query.where(Char.path.in_(paths))
        if elements:
            query = query.where(Char.element.in_(elements))

    result = await session.execute(query)
    runs = result.scalars().all()
    return runs


@router.post("/runs", response_model=dict)
async def submit_run(
    request: RunIn = Body(),
    session: AsyncSession = Depends(get_session),
):
    std_cost_entity = (await session.execute(select(Cost).where(Cost.name.ilike("%Standard%")))).scalars().first()
    ltd_cost_entity = (await session.execute(select(Cost).where(Cost.name.ilike("%Limited%")))).scalars().first()

    units = []
    std_cost, ltd_cost = 0, 0

    for u in request.units:
        unit = Unit(char_id=u.char_id, char_eidolon=u.char_eidolon, lc_id=u.lc_id, lc_superimposition=u.lc_superimposition)
        existing = (await session.execute(
            select(Unit).where(
                Unit.char_id == unit.char_id,
                Unit.char_eidolon == unit.char_eidolon,
                Unit.lc_id == unit.lc_id,
                Unit.lc_superimposition == unit.lc_superimposition
            )
        )).scalars().first()
        if existing:
            unit = existing

        units.append(unit)
        uc_ltd, uc_std = get_unit_cost(unit)
        ltd_cost += uc_ltd
        std_cost += uc_std

    run_costs = [
        RunCost(cost=std_cost_entity, cost_id=std_cost_entity.id, value=std_cost),
        RunCost(cost=ltd_cost_entity, cost_id=ltd_cost_entity.id, value=ltd_cost),
    ]

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
    await session.commit()
    await session.refresh(run)

    return {"run_id": run.id}


@router.delete("/runs/reject/{submission_id}/{rejected_by}")
async def reject_submission(
    submission_id: str,
    rejected_by: str,
    session: AsyncSession = Depends(get_session)
):
    run = (await session.execute(select(Run).where(Run.id == submission_id))).scalars().first()
    if run:
        run.status = RunStatusEnum.Rejected
        run.reviewed_by = rejected_by
        await session.commit()


@router.patch("/runs/approve/{submission_id}/{approved_by}")
async def approve_submission(
    submission_id: str,
    approved_by: str,
    session: AsyncSession = Depends(get_session)
):
    run = (await session.execute(select(Run).where(Run.id == submission_id))).scalars().first()
    if run:
        run.status = RunStatusEnum.Approved
        run.reviewed_by = approved_by
        await session.commit()
