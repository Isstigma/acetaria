from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_session
from app.database.models import Cost
from app.schemas.costs import CostOut

router = APIRouter(tags=["costs"])

@router.get("/costs", response_model=list[CostOut])
async def list_costs(
    session: AsyncSession = Depends(get_session)
):
    result = await session.execute(select(Cost))
    items = result.scalars().all()
    return items
