from typing import Any, AsyncGenerator

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from ..dependencies import AsyncSessionLocal, engine, get_async_session  # noqa
from ..generic_db_repository import CRUDBaseRepository  # noqa
from .data import Base

TEST_DB_URL = 'sqlite+aiosqlite:///./test.db'

test_engine = create_async_engine(TEST_DB_URL,
                                  connect_args={'check_same_thread': False})
TestingSessionLocal = async_sessionmaker(test_engine,
                                         expire_on_commit=False,
                                         autocommit=False,
                                         autoflush=False)
pytest_mark_anyio = pytest.mark.asyncio


@pytest_asyncio.fixture(autouse=True)
async def init_db() -> AsyncGenerator[None, Any]:
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def get_test_session() -> AsyncGenerator[None, Any]:
    async with TestingSessionLocal() as session:
        yield session
