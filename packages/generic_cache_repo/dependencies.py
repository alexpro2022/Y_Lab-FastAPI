from typing import Annotated

from fastapi import Depends
from redis import Redis  # type: ignore [import]
from redis import asyncio as aioredis  # type: ignore [import]

redis_url = 'redis://redis:6379'


def get_aioredis() -> aioredis.Redis:
    return aioredis.from_url(redis_url)


def get_redis():
    return Redis(host='redis', port='6379', db=0)


redis = Annotated[aioredis.Redis, Depends(get_aioredis)]
