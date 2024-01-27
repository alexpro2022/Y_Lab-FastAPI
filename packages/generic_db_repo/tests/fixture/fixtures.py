from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator

import pytest_asyncio
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from .data import BaseTest

TEST_DB_URL = 'postgresql+asyncpg://postgres:test_password@test_db:5432'

test_engine = create_async_engine(TEST_DB_URL, poolclass=NullPool)
TestingSessionLocal = async_sessionmaker(test_engine,
                                         expire_on_commit=False,
                                         autocommit=False,
                                         autoflush=False)


@pytest_asyncio.fixture(autouse=True)
async def init_db() -> AsyncGenerator[None, Any]:
    async with test_engine.begin() as conn:
        await conn.run_sync(BaseTest.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(BaseTest.metadata.drop_all)


@asynccontextmanager
async def test_session() -> AsyncGenerator[None, Any]:
    async with TestingSessionLocal() as session:
        yield session


@pytest_asyncio.fixture
async def get_test_session() -> AsyncGenerator[None, Any]:
    async with test_session() as session:
        yield session
