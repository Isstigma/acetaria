from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from app.core.db import get_session
from app.schemas.games import GameModeEntryOut, GameModeOut
from app.core.models import Cost, GameMode, GameModeEntry
from app.schemas.costs import CostOut

router = APIRouter(tags=["costs"])

@router.get("/costs", response_model=list[CostOut])
async def list_costs(
                     session: Session = Depends(get_session)
                     ):
    items = session.exec(select(Cost)).all()
    return items