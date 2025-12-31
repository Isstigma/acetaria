from fastapi import APIRouter, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.core.db import get_db
from app.schemas.common import Page
from app.schemas.games import GameOut, ModeOut

router = APIRouter(tags=["games"])


@router.get("/games", response_model=Page[GameOut])
async def list_games(page: int = 1, pageSize: int = 50, db: AsyncIOMotorDatabase = Depends(get_db)):
    q = {}
    total = await db.games.count_documents(q)
    cursor = db.games.find(q).skip((page - 1) * pageSize).limit(pageSize)
    items = [GameOut(**doc) async for doc in cursor]
    return Page(items=items, page=page, pageSize=pageSize, total=total)


@router.get("/games/{gameSlug}/modes", response_model=Page[ModeOut])
async def list_modes(gameSlug: str, page: int = 1, pageSize: int = 50, db: AsyncIOMotorDatabase = Depends(get_db)):
    game = await db.games.find_one({"slug": gameSlug})
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")

    q = {"gameSlug": gameSlug}
    total = await db.modes.count_documents(q)
    cursor = db.modes.find(q).skip((page - 1) * pageSize).limit(pageSize)
    items = [ModeOut(**doc) async for doc in cursor]
    return Page(items=items, page=page, pageSize=pageSize, total=total)
