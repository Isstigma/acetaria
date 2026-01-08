from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.routers.games import router as games_router
from app.routers.runs import router as runs_router
from app.routers.admin import router as admin_router
from app.routers.meta import router as meta_router
from app.routers.chars import router as chars_router
from app.routers.lightcones import router as lcs_router
from app.routers.gamemodes import router as gamemodes_router
from app.routers.costs import router as costs_router
from app.seed import ensure_seeded
from app.core.db import init_db
from app.core.models import *

app = FastAPI(title="Acetaria API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(games_router, prefix=settings.api_prefix)
app.include_router(runs_router, prefix=settings.api_prefix)
app.include_router(admin_router, prefix=settings.api_prefix)
app.include_router(meta_router, prefix=settings.api_prefix)
app.include_router(chars_router, prefix=settings.api_prefix)
app.include_router(lcs_router, prefix=settings.api_prefix)
app.include_router(gamemodes_router, prefix=settings.api_prefix)
app.include_router(costs_router, prefix=settings.api_prefix)
# print(settings.model_dump())#todo remove

@app.get("/healthz")
async def healthz():
    return {"ok": True}


@app.on_event("startup")
async def startup_seed():
    init_db()
    if settings.acetaria_auto_seed == 1:
        await ensure_seeded()
