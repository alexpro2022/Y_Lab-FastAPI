import asyncio
from typing import Any, Generic

import pytest
import pytest_asyncio
from deepdiff import DeepDiff
from redis import asyncio as aioredis  # type: ignore [import]

from packages.generic_db_repo.generic_db_repository import ModelType

from ..dependencies import get_aioredis
from ..types import CacheType


class BaseRedisTest(Generic[CacheType, ModelType]):
    cache: type[CacheType]
    model: type[ModelType]
    create_data: dict
    time_expire: int = 1

# instance under test is called `_cache`

# --- Fixtures ---
    @pytest_asyncio.fixture
    async def init(self, get_test_redis) -> None:
        self._cache = self.cache(get_test_redis)

    def test_init_fixture(self, init) -> None:
        assert isinstance(self._cache, self.cache)

    @pytest_asyncio.fixture
    async def init_expire(self, init) -> None:
        self._cache.redis_expire = self.time_expire

    def test_init_expire_fixture(self, init_expire) -> None:
        assert isinstance(self._cache, self.cache)
        assert self._cache.redis_expire == self.time_expire

    @pytest.fixture(scope='class')
    def get_test_obj(self) -> ModelType:
        return self.model(**self.create_data)

    def test_get_test_obj_fixture(self, get_test_obj) -> None:
        assert isinstance(get_test_obj, self.model)

    @pytest_asyncio.fixture
    async def set_cache(self, init, get_test_obj) -> ModelType:
        assert await self._cache_empty()
        await self._cache.set(get_test_obj)
        assert not await self._cache_empty()
        return get_test_obj

    async def test_set_cache_fixture(self, set_cache) -> None:
        from_cache = await self._cache.get(set_cache.id)
        self._compare(from_cache, set_cache)

# --- Tests ---
    @pytest.mark.parametrize('suffix', (1, 1.2, '1', [1, 2], (1, 2), {1, 1, 2}, {'1': 300}))
    def test_get_key(self, init, suffix: Any) -> None:
        key = self._cache._get_key(suffix)
        assert isinstance(key, str)
        assert key == f'{self._cache.key_prefix}{self._cache.delimeter}{suffix}'

    @pytest.mark.parametrize('obj', (b'str', 1, 2.2, 'str', 'get_test_obj'))
    def test_serialize(self, init, obj, request) -> None:
        try:
            obj = request.getfixturevalue(obj)
        except pytest.FixtureLookupError:
            assert self._cache._serialize(obj) == obj
        else:
            assert self._cache._serialize(obj) == self._cache.serializer.dumps(obj)

    @pytest.mark.parametrize('obj', (b'str', 1, 2.2, 'str', 'get_test_obj'))
    def test_deserialize(self, init, obj, request) -> None:
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
        from_cache = await self._cache.get(get_test_obj.id)
        self._compare(from_cache, get_test_obj)

    async def test_cache_expire(self, init_expire, get_test_obj) -> None:
        await self._cache.set([get_test_obj])
        assert not await self._cache_empty()
        await asyncio.sleep(self.time_expire)
        assert await self._cache_empty()

    async def test_delete_obj(self, set_cache) -> None:
        await self._cache.delete(set_cache)
        assert await self._cache_empty()

    async def test_get_returns_None(self, init, get_test_obj) -> None:
        assert await self._cache.get() is None
        assert await self._cache.get(get_test_obj.id) is None

    async def test_get_returns_obj(self, set_cache) -> None:
        from_cache = await self._cache.get(set_cache.id)
        self._compare(from_cache, set_cache)

    async def test_get_returns_list(self, set_cache) -> None:
        from_cache = await self._cache.get()
        assert isinstance(from_cache, list)
        self._compare(from_cache[0], set_cache)

    async def test_get_aioredis(self) -> None:
        assert isinstance(get_aioredis(), aioredis.Redis)

# --- Utils ---
    async def _cache_empty(self) -> bool:
        return await self._cache.get() is None

    @staticmethod
    def _compare(left: Any, right: Any) -> None:
        assert isinstance(left, type(right))
        diff = DeepDiff(left, right, exclude_paths='_sa_instance_state')
        assert not diff, diff
