import json
from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from app.core.db import get_session
from app.schemas.games import GameModeEntryOut, GameModeOut
from app.core.models import Cost, GameMode, GameModeEntry, EventFreeCharacter
from app.schemas.costs import CostOut, FreeCharactersResponse 
from sqlalchemy.ext.asyncio import AsyncSession 

router = APIRouter(tags=["costs"])

@router.get("/costs", response_model=list[CostOut])
async def list_costs(
                     session: AsyncSession = Depends(get_session)
                     ):
    items = (await session.execute(select(Cost))).scalars().all()
    return items


@router.get("/free-characters")
async def get_free_characters(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(EventFreeCharacter))
    events = result.scalars().all()
    output = []
    for ev in events:
        output.append({
            "event_name": ev.event_name,
            "pool": ev.character_names
        })
    return output
