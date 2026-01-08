from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from app.core.db import get_session
from app.core.models import Lightcone

router = APIRouter(tags=["lightcones"])

@router.get("/games/{gameSlug}/lightcones", response_model=list[Lightcone]) 
async def list_lcs(gameSlug: str, session: Session = Depends(get_session)):
    items = session.exec(select(Lightcone)).all()
    return items
