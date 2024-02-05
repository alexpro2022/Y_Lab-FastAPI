from typing import Any, AsyncGenerator

import pytest_asyncio
from fakeredis.aioredis import FakeRedis


@pytest_asyncio.fixture
async def get_test_redis() -> AsyncGenerator[FakeRedis, Any]:
    r = FakeRedis()
    yield r
    await r.flushall()
