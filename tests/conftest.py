from typing import Any, AsyncGenerator

import pytest
from fakeredis.aioredis import FakeRedis

from app.main import app
from packages.generic_cache_repo.dependencies import get_aioredis
from packages.generic_db_repo.dependencies import get_async_session
from packages.generic_db_repo.testing_tools.db import TestingSessionLocal

pytest_plugins = [
    'tests.fixtures.fixtures',
]

pytest_mark_anyio = pytest.mark.asyncio
# pytest_mark_anyio = pytest.mark.anyio


async def override_get_async_session() -> AsyncGenerator[Any, None]:
    async with TestingSessionLocal() as session:
        yield session


async def override_get_aioredis() -> AsyncGenerator[FakeRedis, Any]:
    r = FakeRedis()
    await r.flushall()
    return r


app.dependency_overrides[get_async_session] = override_get_async_session
app.dependency_overrides[get_aioredis] = override_get_aioredis
