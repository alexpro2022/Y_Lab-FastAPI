from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (AsyncEngine, AsyncSession,
                                    async_sessionmaker)

from ...generic_db_repo.dependencies import (AsyncSessionLocal, engine,
                                             get_async_session)


def test_engine() -> None:
    assert isinstance(engine, AsyncEngine)


def test_async_session_local() -> None:
    assert isinstance(AsyncSessionLocal, async_sessionmaker)


async def test_get_async_session() -> None:
    agen = get_async_session()
    assert isinstance(agen, AsyncGenerator)
    async_session = await anext(agen)
    assert isinstance(async_session, AsyncSession)
