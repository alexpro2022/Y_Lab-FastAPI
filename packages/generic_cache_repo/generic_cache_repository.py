import pickle
from typing import Any
from redis import asyncio as aioredis  # type: ignore [import]

from .dependencies import redis

# KeyType: TypeAlias = str | uuid.UUID


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

    async def get_keys(self, redis: aioredis.Redis, pattern: str):
        return [key.decode('utf-8') for key in await redis.keys(pattern)]

    async def get(self, key: Any | None = None, pattern: str = '*') -> Any | list[Any] | None:
        async def get_obj(key: Any) -> Any | None:
            cache = await self.redis.get(key)
            return self._deserialize(cache) if cache else None

        if key is None:  # get all from the group specified by self.key_prefix
            result = [await get_obj(key) for key in await self.get_keys(self.redis, f'{self.key_prefix}{pattern}')]
            return result if result and None not in result else None
        # the cache key for that obj might contain the parent id, so need to get it via pattern
        keys = await self.get_keys(self.redis, f'{self._get_key(key)}*')
        return None if not keys else await get_obj(keys[0])

    async def set(self, entity: Any | list[Any]) -> None:
        """Sets the obj(s) to cache as a dict(s)."""
        async def set_obj(obj: Any) -> None:
            parent_id = getattr(obj, self.parent_id_field_name, None)
            # create the cache key proto as: obj_id:parent_id
            key = obj.id if parent_id is None else f'{obj.id}:{parent_id}'
            obj = obj if isinstance(obj, dict) else obj._asdict()
            # obj = self._asdict(obj)
            await self.redis.set(self._get_key(key), self._serialize(obj), ex=self.redis_expire)

        if isinstance(entity, (list, tuple)):
            for obj in entity:
                await set_obj(obj)
        else:
            await set_obj(entity)

    async def delete(self, obj: Any) -> None:
        # the cache key for that obj might contain the parent id, so need to get it via pattern
        keys = await self.get_keys(self.redis, f'{self._get_key(obj.id)}*')
        if keys:
            await self.redis.delete(self._get_key(keys[0]))

    '''@staticmethod
    def _asdict(obj: Any) -> dict[str, Any]:
        return obj if isinstance(obj, dict) else obj._asdict()'''
