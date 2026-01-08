from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from app.core.db import get_session
from app.schemas.common import Page
from app.schemas.games import GameOut
from app.core.models import Char

router = APIRouter(tags=["games"])


@router.get("/games", response_model=Page[GameOut])
async def list_games(page: int = 1, pageSize: int = 50, 
                     session: Session = Depends(get_session)
                     ):
    q = {}
    # total = await db.games.count_documents(q)
    # cursor = db.games.find(q).skip((page - 1) * pageSize).limit(pageSize)
    # items = [GameOut(**doc) async for doc in cursor]
    items = session.exec(select(Char)).all()
    return Page(items=items, page=page, pageSize=pageSize, total=0)#todo total


# @router.get("/games/{gameSlug}/modes", response_model=Page[ModeOut])
# async def list_modes(gameSlug: str, page: int = 1, pageSize: int = 50, 
#                      #db: AsyncIOMotorDatabase = Depends(get_db)
#                      ):
    # game = await db.games.find_one({"slug": gameSlug})
    # if not game:
    #     raise HTTPException(status_code=404, detail="Game not found")

    # q = {"gameSlug": gameSlug}
    # total = await db.modes.count_documents(q)
    # cursor = db.modes.find(q).skip((page - 1) * pageSize).limit(pageSize)
    # items = [ModeOut(**doc) async for doc in cursor]
    # return Page(items=[], page=0, pageSize=0, total=0)#todo
