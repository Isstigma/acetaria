from datetime import datetime
import json
from typing import Optional
import aiohttp
from fastapi import APIRouter, Body, Depends, HTTPException, Query
from sqlalchemy import nulls_last, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import contains_eager, selectinload

from app.core.auth import get_current_user, require_moderator_or_admin
from app.core.db import get_session
from app.core.enums import ElementEnum, PathEnum, ResultFlags, ResultKindEnum, RunStatusEnum
from app.core.models import Char, Cost, GameMode, GameModeEntry, Run, RunCost, Team, Unit, User
from app.schemas.runs import RunIn, RunWithTeamOut

WEBHOOK_URL = 'https://discord.com/api/webhooks/placeholder'

router = APIRouter(tags=['runs'])


def getUnitCost(unit: Unit) -> tuple[int, int]:
    std_cost = 1
    ltd_cost = 0

    if unit.char_eidolon is not None and unit.char_eidolon > 0:
        ltd_cost += unit.char_eidolon
    if unit.lc_id is not None:
        ltd_cost += 1
        if unit.lc_superimposition is not None and unit.lc_superimposition > 1:
            ltd_cost += unit.lc_superimposition - 1
    return std_cost, ltd_cost


@router.get('/runs-status')
async def get_runs_status(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(require_moderator_or_admin),
):
    query = select(Run.status, Run.id).order_by(Run.submitted_at.desc())
    results = (await session.execute(query)).all()
    return [{"id": row.id, "status": row.status} for row in results]


@router.get('/runs/{stage_id}', response_model=list[RunWithTeamOut])
async def get_runs_for_stage(
    stage_id: int,
    session: AsyncSession = Depends(get_session),
):
    query = (
        select(Run)
        .join(Run.game_mode_entry)
        .join(GameModeEntry.game_mode)
        .join(Run.team)
        .outerjoin(Team.units)
        .join(Unit.char)
        .outerjoin(Unit.lc)
        .where(Run.game_mode_entry_id == stage_id, Run.status == RunStatusEnum.Approved)
        .options(
            contains_eager(Run.game_mode_entry).contains_eager(GameModeEntry.game_mode),
            contains_eager(Run.team)
            .contains_eager(Team.units)
            .contains_eager(Unit.char),
            contains_eager(Run.team)
            .contains_eager(Team.units)
            .contains_eager(Unit.lc),
            selectinload(Run.run_costs).selectinload(RunCost.cost),
        )
    )
    runs = (await session.execute(query)).unique().scalars().all()
    return runs


@router.get('/runs')
async def get_runs(
    include_pending: bool = Query(False),
    session: AsyncSession = Depends(get_session),
    chars: list[int] | None = Query(None),
    elements: list[ElementEnum] | None = Query(None),
    paths: list[PathEnum] | None = Query(None),
    refs: list[str] | None = Query(None),
    name: Optional[str] = None,
    stage_id: Optional[int] = None,
    id: Optional[str] = None,
    author_name: Optional[str] = None,
):
    query = (
        select(Run)
        .join(Run.game_mode_entry)
        .join(GameModeEntry.game_mode)
        .join(Run.team)
        .outerjoin(Team.units)
        .join(Unit.char)
        .outerjoin(Unit.lc)
        .options(
            contains_eager(Run.game_mode_entry).contains_eager(GameModeEntry.game_mode),
            contains_eager(Run.team).contains_eager(Team.units).contains_eager(Unit.char),
            contains_eager(Run.team).contains_eager(Team.units).contains_eager(Unit.lc),
            selectinload(Run.run_costs).selectinload(RunCost.cost),
        )
    )

    if refs is not None:
        query = query.where(Run.submission_ref.in_(refs))

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

    if name is not None:
        query = query.where(Run.name.ilike(f"%{name}%"))

    runs = (await session.execute(query)).unique().scalars().all()
    return runs


@router.post('/runs')
async def submit_run(
    session: AsyncSession = Depends(get_session),
    request: RunIn = Body(),
    current_user: User = Depends(get_current_user),
):
    units = []
    std_cost = 0
    ltd_cost = 0
    std_cost_entity = (await session.execute(select(Cost).where(Cost.name.ilike("%Standard%")))).scalar_one()
    ltd_cost_entity = (await session.execute(select(Cost).where(Cost.name.ilike("%Limited%")))).scalar_one()

    for i, unit_in in enumerate(request.units):
        unit = Unit(
            char_id=unit_in.char_id,
            char_eidolon=unit_in.char_eidolon,
            lc_id=unit_in.lc_id,
            lc_superimposition=unit_in.lc_superimposition,
            is_main=(i == 0),
        )
        existing_unit = (
            await session.execute(
                select(Unit).filter_by(
                    char_id=unit.char_id,
                    char_eidolon=unit.char_eidolon,
                    lc_id=unit.lc_id,
                    lc_superimposition=unit.lc_superimposition,
                    is_main=unit.is_main,
                )
            )
        ).scalar_one_or_none()
        if existing_unit:
            unit = existing_unit
        units.append(unit)
        unit_std_cost, unit_ltd_cost = getUnitCost(unit)
        std_cost += unit_std_cost
        ltd_cost += unit_ltd_cost

    run_costs: list[RunCost] = [
        RunCost(cost=std_cost_entity, cost_id=std_cost_entity.id, value=std_cost),
        RunCost(cost=ltd_cost_entity, cost_id=ltd_cost_entity.id, value=ltd_cost),
    ]

    team = Team(name=request.name)
    session.add(team)
    session.add_all(units)
    await session.commit()
    await session.refresh(team)
    for unit in units:
        await session.refresh(unit)
    team.units = units

    submitted_by = current_user.global_name or current_user.username
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
        submitted_by=submitted_by,
        run_costs=run_costs,
        submission_ref=request.submission_ref,
    )

    session.add(run)
    await session.commit()
    await session.refresh(run)

    session.add_all(run_costs)
    await session.commit()

    try:
        if getattr(request, 'embed_discord', None):
            with aiohttp.MultipartWriter('form-data') as mp:
                request_content = json.dumps({"embeds": [json.loads(request.embed_discord)], "content": str(run.id)})
                part = mp.append(request_content)
                part.set_content_disposition('form-data', name='payload_json')
                async with aiohttp.ClientSession() as client_session:
                    async with client_session.post(WEBHOOK_URL, data=mp) as resp:
                        if not resp.ok:
                            try:
                                print(await resp.json())
                            except Exception:
                                print(await resp.text())
    except Exception as e:
        print(f"Error in /submit: {e}")

    return {"run_id": run.id}


@router.patch('/runs/reject/{submissionId}/{rejectedBy}')
async def reject_submission(
    submissionId: str,
    rejectedBy: str,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(require_moderator_or_admin),
):
    run = (await session.execute(select(Run).where(Run.id == submissionId))).scalar_one_or_none()
    if not run:
        raise HTTPException(status_code=404, detail='Run not found')
    run.status = RunStatusEnum.Rejected
    run.reviewed_by = current_user.id
    run.reviewed_at = datetime.utcnow()
    session.add(run)
    await session.commit()
    await session.refresh(run)
    return {"ok": True, "reviewed_by": current_user.id, "ignored_path_rejected_by": rejectedBy}


@router.patch('/runs/approve/{submissionId}/{approvedBy}')
async def approve_submission(
    submissionId: str,
    approvedBy: str,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(require_moderator_or_admin),
):
    run = (await session.execute(select(Run).where(Run.id == submissionId))).scalar_one_or_none()
    if not run:
        raise HTTPException(status_code=404, detail='Run not found')
    run.status = RunStatusEnum.Approved
    run.reviewed_by = current_user.id
    run.reviewed_at = datetime.utcnow()
    session.add(run)
    await session.commit()
    await session.refresh(run)
    return {"ok": True, "reviewed_by": current_user.id, "ignored_path_approved_by": approvedBy}
