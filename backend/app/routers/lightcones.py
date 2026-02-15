from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_session
from app.database.models import Lightcone
from app.schemas.lightcones import LightconeOut

router = APIRouter(tags=["lightcones"])


@router.get("/games/{gameSlug}/lightcones", response_model=list[LightconeOut])
async def list_lcs(
    gameSlug: str,
    session: AsyncSession = Depends(get_session)
):
    result = await session.execute(select(Lightcone))
    items = result.scalars().all()
    return items
