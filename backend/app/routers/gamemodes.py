from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from app.core.db import get_session
from app.schemas.games import GameModeEntryOut, GameModeOut
from app.core.models import GameMode, GameModeEntry
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

router = APIRouter(tags=["gamemodes"])


@router.get("/games/{gameSlug}/modes", response_model=list[GameModeOut])
async def list_modes(gameSlug: str,
                     session: AsyncSession = Depends(get_session)
                     ):
    query = select(GameMode).options(selectinload(GameMode.game_mode_entries))
    print(query)
    items = (await session.execute(query)).scalars().all()
    return items
