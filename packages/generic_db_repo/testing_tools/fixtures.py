from typing import Any, AsyncGenerator

import pytest_asyncio

from ..base import Base as TestBase
from .db import TestingSessionLocal, test_engine


@pytest_asyncio.fixture
async def init_db() -> AsyncGenerator[None, Any]:
    async with test_engine.begin() as conn:
        await conn.run_sync(TestBase.metadata.create_all)
    yield 'init_db'
    async with test_engine.begin() as conn:
        await conn.run_sync(TestBase.metadata.drop_all)


@pytest_asyncio.fixture
async def get_test_session() -> AsyncGenerator[None, Any]:
    async with TestingSessionLocal() as session:
        yield session
