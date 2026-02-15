from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.seed import ensure_seeded
from app.database.models import *
from app.database.session import init_db
from app.routers import ROUTERS


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    if settings.auto_seed:
        await ensure_seeded()
    yield


app = FastAPI(
    title="Acetaria API",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True, 
    allow_methods=settings.cors_methods,
    allow_headers=settings.cors_headers,
)

for router in ROUTERS:
    app.include_router(router, prefix=settings.api_prefix)


@app.get("/healthz")
async def healthz():
    return {"ok": True}
