from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from app.core.db import get_session
from app.core.models import Char
from sqlalchemy.ext.asyncio import AsyncSession as _AsyncSession

router = APIRouter(tags=["chars"])

@router.get("/games/{gameSlug}/chars", response_model=list[Char])
async def list_chars(gameSlug: str,
                     session: _AsyncSession = Depends(get_session)
                     ):
    items = (await session.execute(select(Char))).scalars().all()
    return items
