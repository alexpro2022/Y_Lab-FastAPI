import pickle
from typing import Any

from redis import asyncio as aioredis  # type: ignore [import]

# from app.core.config import settings
# redis_url = settings.redis_url

redis_url = 'redis://redis:6379'


def get_aioredis() -> aioredis.Redis:
    return aioredis.from_url(redis_url)


class BaseRedis:

    def __init__(self,
                 redis: aioredis.Redis,
                 redis_key_prefix_with_delimeter: str = ':',
                 redis_expire: int = 3600, serializer=pickle) -> None:
        self.redis = redis
        self.redis_key_prefix = redis_key_prefix_with_delimeter
        self.redis_expire = redis_expire
        self.serializer = serializer

    def _get_key(self, key: Any) -> str:
        return f'{self.redis_key_prefix}{key}'

    def _serialize(self, obj) -> bytes | str | int | float:
        """Pickle if an object is not of type of a bytes, string, int or float."""
        return obj if isinstance(obj, (bytes, str, int, float)) else self.serializer.dumps(obj)

    def _deserialize(self, cache) -> bytes | str | int | float | Any:
        """Unpickle if an object is not of type of a bytes, string, int or float."""
        if isinstance(cache, (str, int, float)):
            return cache
        try:
            return self.serializer.loads(cache)
        except pickle.UnpicklingError:
            return cache

    async def get(self, key: Any | None = None) -> Any | list[Any] | None:
        async def get_obj(key: Any) -> Any | None:
            key = (key if (isinstance(key, str) and key.startswith(self.redis_key_prefix))
                   else self._get_key(key))
            cache = await self.redis.get(key)
            return self._deserialize(cache) if cache else None

        if key is None:
            result = [await get_obj(key.decode('utf-8')) for key in
                      await self.redis.keys(f'{self.redis_key_prefix}*')]
            return result if result and None not in result else None
        return await get_obj(key)

    async def set(self, entity: Any | list[Any]) -> None:
        async def set_obj(obj: Any) -> None:
            await self.redis.set(self._get_key(obj.id), self._serialize(obj), ex=self.redis_expire)

        if isinstance(entity, (list, tuple)):
            for obj in entity:
                await set_obj(obj)
        else:
            await set_obj(entity)

    async def delete(self, obj: Any) -> None:
        await self.redis.delete(self._get_key(obj.id))
