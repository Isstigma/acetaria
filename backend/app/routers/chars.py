from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from app.core.db import get_session
from app.core.models import Char

router = APIRouter(tags=["chars"])

@router.get("/games/{gameSlug}/chars", response_model=list[Char])
async def list_chars(gameSlug: str,
                     session: Session = Depends(get_session)
                     ):
    items = session.exec(select(Char)).all()
    return items
