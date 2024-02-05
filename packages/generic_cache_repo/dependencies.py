from typing import Annotated

from fastapi import Depends
from redis import asyncio as aioredis  # type: ignore [import]

redis_url = 'redis://redis:6379'


def get_aioredis() -> aioredis.Redis:
    return aioredis.from_url(redis_url)


redis = Annotated[aioredis.Redis, Depends(get_aioredis)]
