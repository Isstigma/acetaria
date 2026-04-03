from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from app.core.db import get_session
from app.core.models import Lightcone
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(tags=["lightcones"])

@router.get("/games/{gameSlug}/lightcones", response_model=list[Lightcone]) 
async def list_lcs(gameSlug: str, session: AsyncSession = Depends(get_session)):
    items = (await session.execute(select(Lightcone))).scalars().all()
    return items
