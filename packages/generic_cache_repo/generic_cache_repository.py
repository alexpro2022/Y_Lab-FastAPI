import pickle
from typing import Any

from .dependencies import redis


class BaseRedis:
    key_prefix: str
    parent_id_field_name: str = 'None'
    delimeter: str = ':'
    redis_expire: int = 3600
    serializer = pickle

    def __init__(self, redis: redis) -> None:
        self.redis = redis

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

    def _get_key(self, key: Any) -> str:
        if isinstance(key, str) and key.startswith(self.key_prefix):
            return key
        return f'{self.key_prefix}{self.delimeter}{key}'

    async def get(self, key: Any | None = None, pattern: str = '*') -> Any | list[Any] | None:
        async def get_obj(key: Any) -> Any | None:
            cache = await self.redis.get(key)
            return self._deserialize(cache) if cache else None

        if key is None:
            result = [await get_obj(key.decode('utf-8')) for key in
                      await self.redis.keys(f'{self.key_prefix}{pattern}')]
            return result if result and None not in result else None
        pattern = f'{self._get_key(key)}*'
        keys = [key.decode('utf-8') for key in await self.redis.keys(pattern)]
        return None if not keys else await get_obj(keys[0])

    async def set(self, entity: Any | list[Any]) -> None:
        async def set_obj(obj: Any) -> None:
            parent_id = getattr(obj, self.parent_id_field_name, None)
            key = obj.id if parent_id is None else f'{obj.id}:{parent_id}'
            await self.redis.set(self._get_key(key), self._serialize(obj), ex=self.redis_expire)

        if isinstance(entity, (list, tuple)):
            for obj in entity:
                await set_obj(obj)
        else:
            await set_obj(entity)

    async def delete(self, obj: Any) -> None:
        pattern = f'{self._get_key(obj.id)}*'
        keys = [key.decode('utf-8') for key in await self.redis.keys(pattern)]
        print(keys)
        if keys:
            await self.redis.delete(self._get_key(keys[0]))
