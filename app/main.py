'''
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI

from app.api import main_router

from app.core import create_admin, get_async_session, settings


@asynccontextmanager
async def lifespan(app: FastAPI, async_session: AsyncGenerator = get_async_session):
    yield   # await create_admin(async_session)


app = FastAPI(lifespan=lifespan,
              title=settings.app_title,
              description=settings.app_description)

app.include_router(main_router)
'''
