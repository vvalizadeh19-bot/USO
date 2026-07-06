"""FastAPI application entrypoint for the USO Enterprise Platform backend."""
from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes import auth, cpm, dashboard, work_items
from app.core.config import settings
from app.core.init_db import init


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables and seed baseline data on startup (dev convenience).
    init()
    yield


app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="USO Enterprise Platform (UEP) — backend API.",
    lifespan=lifespan,
)


@app.get("/health", tags=["system"])
def health() -> dict[str, str]:
    return {"status": "ok", "environment": settings.environment}


for r in (auth.router, work_items.router, dashboard.router, cpm.router):
    app.include_router(r, prefix=settings.api_prefix)
