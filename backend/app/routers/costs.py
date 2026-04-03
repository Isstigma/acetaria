from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from app.core.db import get_session
from app.schemas.games import GameModeEntryOut, GameModeOut
from app.core.models import Cost, GameMode, GameModeEntry
from app.schemas.costs import CostOut
from sqlalchemy.ext.asyncio import AsyncSession 

router = APIRouter(tags=["costs"])

@router.get("/costs", response_model=list[CostOut])
async def list_costs(
                     session: AsyncSession = Depends(get_session)
                     ):
    items = (await session.execute(select(Cost))).scalars().all()
    return items