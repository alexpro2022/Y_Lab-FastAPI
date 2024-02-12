from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator

from fastapi import FastAPI

from app.api.routers import main_router
from app.celery_tasks.utils import load_data
from app.core.config import settings
from packages.generic_db_repo.base import Base
from packages.generic_db_repo.dependencies import engine


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, Any]:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    await load_data()
    yield


app = FastAPI(title=settings.app_title,
              description=settings.app_description,
              lifespan=lifespan)

app.include_router(main_router)
