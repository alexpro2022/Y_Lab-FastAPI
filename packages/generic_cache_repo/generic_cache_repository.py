import pickle
import uuid
from typing import Any, TypeAlias

from .dependencies import redis

KeyType: TypeAlias = str | uuid.UUID


class BaseRedis:
    key_prefix: str
    delimeter: str = ':'
    redis_expire: int = 3600
    serializer = pickle

    def __init__(self, redis: redis) -> None:
        self.redis = redis

    def _get_key(self, key: KeyType) -> str:
        return (key if (isinstance(key, str) and key.startswith(self.key_prefix)) else
                f'{self.key_prefix}{self.delimeter}{key}')

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

    async def get(self, key: KeyType | None = None, pattern: str = '*') -> Any | list[Any] | None:
        async def get_obj(key: KeyType) -> Any | None:
            key = self._get_key(key)
            print(key)
            cache = await self.redis.get(key)
            return self._deserialize(cache) if cache else None

        if key is None:
            result = [await get_obj(key.decode('utf-8')) for key in
                      await self.redis.keys(f'{self.key_prefix}{pattern}')]
            return result if result and None not in result else None
        return await get_obj(key)

    @staticmethod
    def create_key(obj: dict[str, Any]) -> str:
        return f"{obj['id']}"

    async def set(self, entity: Any | list[Any]) -> None:
        """Sets the obj(s) to cache as a dict(s)."""
        async def set_obj(obj: Any) -> None:
            obj = self._asdict(obj)
            key = self.create_key()
            await self.redis.set(self._get_key(key), self._serialize(obj), ex=self.redis_expire)

        if isinstance(entity, (list, tuple)):
            for obj in entity:
                await set_obj(obj)
        else:
            await set_obj(entity)

    async def delete(self, obj: Any) -> None:
        await self.redis.delete(self._get_key(self._asdict(obj)['id']))

    @staticmethod
    def _asdict(obj: Any) -> dict[str, Any]:
        return obj if isinstance(obj, dict) else obj._asdict()
