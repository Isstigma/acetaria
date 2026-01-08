from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from app.core.db import get_session
from app.schemas.games import GameModeEntryOut, GameModeOut
from app.core.models import GameMode, GameModeEntry

router = APIRouter(tags=["gamemodes"])


@router.get("/games/{gameSlug}/modes", response_model=list[GameModeOut])
async def list_modes(gameSlug: str,
                     session: Session = Depends(get_session)
                     ):
    items = session.exec(select(GameMode)).all()
    return items
