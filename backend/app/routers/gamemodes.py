from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_session
from app.database.models import GameMode
from app.schemas.games import GameModeOut

router = APIRouter(tags=["gamemodes"])

@router.get("/games/{gameSlug}/modes", response_model=list[GameModeOut])
async def list_modes(
    gameSlug: str,
    session: AsyncSession = Depends(get_session)
):
    result = await session.execute(select(GameMode)
        .options(selectinload(GameMode.game_mode_entries))
    )
    items = result.scalars().all()
    return items
