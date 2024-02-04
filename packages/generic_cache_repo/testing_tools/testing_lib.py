import asyncio
from typing import Any, Generic, TypeAlias, TypeVar

import pytest
import pytest_asyncio
from redis import asyncio as aioredis  # type: ignore [import]

from packages.generic_db_repo.generic_db_repository import ModelType

from ..dependencies import get_aioredis
from ..generic_cache_repository import BaseRedis

_CacheType = TypeVar('_CacheType', bound=BaseRedis)
CacheType: TypeAlias = type[_CacheType]


class BaseRedisTest(Generic[_CacheType]):
    cache: CacheType
    model: ModelType
    create_data: dict
    time_expire = 1

# --- Fixtures ---
    @pytest_asyncio.fixture
    async def init(self, get_test_redis) -> None:
        self._cache = self.cache(get_test_redis)  # BaseRedis(get_test_redis, self.prefix)

    def test_init_fixture(self, init) -> None:
        assert isinstance(self._cache, self.cache)

    @pytest_asyncio.fixture
    async def init_expire(self, get_test_redis) -> None:
        self._cache = self.cache(get_test_redis, redis_expire=self.time_expire)

    def test_init_expire_fixture(self, init_expire) -> None:
        assert isinstance(self._cache, self.cache)
        assert self._cache.redis_expire == self.time_expire

    @pytest.fixture
    def get_test_obj(self) -> Any:
        return self.model(**self.create_data)   # type: ignore [arg-type]

    def test_get_test_obj_fixture(self, get_test_obj) -> None:
        assert isinstance(get_test_obj, self.model)
        assert get_test_obj.id == self.create_data['id']
        assert get_test_obj.title == self.create_data['title']
        assert get_test_obj.description == self.create_data['description']

# --- Tests ---
    @pytest.mark.parametrize('suffix', (1, 1.2, '1', [1, 2], (1, 2), {1, 1, 2}, {'1': 300}))
    def test_get_key(self, init, suffix: Any) -> None:
        key = self._cache._get_key(suffix)
        assert isinstance(key, str)
        assert key == f'{self._cache.redis_key_prefix}{suffix}'

    @pytest.mark.parametrize('obj', (b'str', 1, 2.2, 'str', 'get_test_obj'))
    def test_serialize(self, init, obj, request):
        try:
            obj = request.getfixturevalue(obj)
        except pytest.FixtureLookupError:
            assert self._cache._serialize(obj) == obj
        else:
            assert self._cache._serialize(obj) == self._cache.serializer.dumps(obj)

    @pytest.mark.parametrize('obj', (b'str', 1, 2.2, 'str', 'get_test_obj'))
    def test_deserialize(self, init, obj, request):
        try:
            obj = request.getfixturevalue(obj)
        except pytest.FixtureLookupError:
            assert self._cache._deserialize(obj) == obj
        else:
            cache = self._cache.serializer.dumps(obj)
            self._compare(self._cache._deserialize(cache), obj)

    @pytest.mark.parametrize('entity', ('single', 'list', 'tuple'))
    async def test_set_obj(self, init, get_test_obj, entity) -> None:
        match entity:
            case 'single':
                arg = get_test_obj
            case 'list':
                arg = [get_test_obj]
            case 'tuple':
                arg = (get_test_obj,)
        assert await self._cache_empty()
        await self._cache.set(arg)
        assert not await self._cache_empty()
        from_cache = await self._cache.get(get_test_obj.id)
        self._compare(from_cache, get_test_obj)

    async def test_cache_expire(self, init_expire, get_test_obj) -> None:
        await self._cache.set([get_test_obj])
        assert not await self._cache_empty()
        await asyncio.sleep(self.time_expire)
        assert await self._cache_empty()

    async def test_delete_obj(self, init, get_test_obj) -> None:
        await self._cache.set(get_test_obj)
        assert not await self._cache_empty()
        await self._cache.delete(get_test_obj)
        assert await self._cache_empty()

    async def test_get_returns_None(self, init, get_test_obj) -> None:
        assert await self._cache.get() is None
        assert await self._cache.get(get_test_obj.id) is None

    async def test_get_returns_obj(self, init, get_test_obj) -> None:
        await self._cache.set(get_test_obj)
        obj = await self._cache.get(get_test_obj.id)
        self._compare(obj, get_test_obj)

    async def test_get_returns_list(self, init, get_test_obj) -> None:
        await self._cache.set(get_test_obj)
        objs = await self._cache.get()
        assert isinstance(objs, list)
        self._compare(objs[0], get_test_obj)

    async def test_get_aioredis(self):
        assert isinstance(get_aioredis(), aioredis.Redis)

# --- Utils ---
    async def _cache_empty(self) -> bool:
        return await self._cache.get() is None

    @staticmethod
    def _compare(left: Any, right: Any) -> None:
        def clean(item) -> dict:
            wanted = '_sa_instance_state'
            d = vars(item).copy()
            if wanted in d:
                d.pop(wanted)
            return d

        assert isinstance(left, type(right))
        assert clean(left) == clean(right)
