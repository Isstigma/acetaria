from fastapi import APIRouter, Depends
from sqlalchemy import distinct
from sqlalchemy import select as sa_select
from sqlmodel import Session, select
from app.core.db import get_session
from app.core.models import Char, Unit, TeamUnitLink, Team, Run
from app.core.enums import RunStatusEnum
from sqlalchemy.ext.asyncio import AsyncSession as _AsyncSession

router = APIRouter(tags=["chars"])

@router.get("/games/{gameSlug}/chars", response_model=list[Char])
async def list_chars(gameSlug: str,
                     session: _AsyncSession = Depends(get_session)
                     ):
    items = (await session.execute(select(Char))).scalars().all()
    return items

@router.get("/games/{gameSlug}/active-ids")
async def get_active_ids(
    gameSlug: str,
    session: _AsyncSession = Depends(get_session)
) -> dict:
    char_stmt = (
        sa_select(distinct(Unit.char_id))
        .join(TeamUnitLink, TeamUnitLink.unit_id == Unit.id)
        .join(Team, Team.id == TeamUnitLink.team_id)
        .join(Run, Run.team_id == Team.id)
        .where(Run.status == RunStatusEnum.Approved)
        .where(Unit.char_id.is_not(None))
    )

    lc_stmt = (
        sa_select(distinct(Unit.lc_id))
        .join(TeamUnitLink, TeamUnitLink.unit_id == Unit.id)
        .join(Team, Team.id == TeamUnitLink.team_id)
        .join(Run, Run.team_id == Team.id)
        .where(Run.status == RunStatusEnum.Approved)
        .where(Unit.lc_id.is_not(None))
    )

    char_ids = list((await session.execute(char_stmt)).scalars().all())
    lc_ids = list((await session.execute(lc_stmt)).scalars().all())

    return {"char_ids": char_ids, "lc_ids": lc_ids}
