from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_session
from app.database.models import Char
from app.schemas.chars import CharOut

router = APIRouter(tags=["chars"])

@router.get("/games/{gameSlug}/chars", response_model=list[CharOut]) #TODO: Is there anything else planned besides HSR?
async def list_chars(
    gameSlug: str,
    session: AsyncSession = Depends(get_session)
):
    result = await session.execute(select(Char))
    items = result.scalars().all()
    return items
