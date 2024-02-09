from uuid import uuid4

import pytest
import pytest_asyncio
from fakeredis import FakeRedis
from fastapi import BackgroundTasks, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from packages.generic_cache_repo.generic_cache_repository import BaseRedis
from packages.generic_db_repo.generic_db_repository import BaseCRUD
from packages.generic_service_repo.generic_service_repository import BaseService
from packages.testing_tools.base_testing_class import BaseTestingClass

PLURAL = 'plural'
SINGLE_PLURAL_ARGS = ('args', ('single', PLURAL))
ID = uuid4()


class BaseServiceTest(BaseTestingClass):
    service = BaseService
    db: BaseCRUD
    cache: BaseRedis

# Instance under test is called _service

# --- Fixtures ---
    @pytest_asyncio.fixture(autouse=True)
    async def init(self, init_db, get_test_session: AsyncSession, get_test_redis: FakeRedis) -> None:
        self._service: BaseService = self.service(
            self.db(get_test_session),
            self.cache(get_test_redis),
        )

    def test_init_fixture(self) -> None:
        assert isinstance(self._service, self.service)
        assert isinstance(self._service.db, self.db)
        assert isinstance(self._service.cache, self.cache)
        assert self._service.bg_tasks is None

    @pytest_asyncio.fixture
    async def get_obj_db(self):
        obj = await self._service.db.create(**self.create_data)
        return await self._service.db.get(id=obj.id)

    async def test_get_obj_db_fixture(self, get_obj_db) -> None:
        self.compare_obj_data(get_obj_db, self.create_data)
        from_db = await self._service.db.get(id=get_obj_db.id)
        self.compare_objs(from_db, get_obj_db)

    @pytest_asyncio.fixture
    async def get_obj_cache(self):
        obj = self._service.db.model(**self.create_data, id=ID)
        await self._service.cache.set(obj)
        return obj

    async def test_get_obj_cache_fixture(self, get_obj_cache):
        from_cache = await self._service.cache.get(key=get_obj_cache.id)
        self.compare_objs(from_cache, get_obj_cache)

# --- Utils ---
    async def _db_empty(self) -> bool:
        return await self._is_empty(self._service.db)

    async def _cache_empty(self) -> bool:
        return await self._is_empty(self._service.cache)

    async def _cache_equals_db(self) -> bool:
        db = await self._service.db.get()
        cache = await self._service.cache.get()
        assert db and cache
        self.compare_lists(db, cache)
        return True

# --- Tests ---
    @pytest.mark.parametrize(*SINGLE_PLURAL_ARGS)
    async def test_add_bg_task_or_execute_executes(self, get_obj_db, args) -> None:
        test_func = self._service.cache.set
        test_args = [get_obj_db] if args == PLURAL else get_obj_db

        assert self._service.bg_tasks is None
        assert await self._cache_empty()
        await self._service._add_bg_task_or_execute(test_func, test_args)
        assert not await self._cache_empty()
        from_cache = await self._service.cache.get()
        assert isinstance(from_cache, list)
        self.compare_objs(from_cache[0], get_obj_db)

    @pytest.mark.parametrize(*SINGLE_PLURAL_ARGS)
    async def test_add_bg_task_or_execute_adds(self, monkeypatch, get_obj_db, args) -> None:
        def mock(_self, func, *args, **kwargs):
            assert isinstance(_self, BackgroundTasks)
            assert func == test_func, (func, test_func)
            assert isinstance(args, tuple)
            assert args[0] == test_args, (args, test_args)
            raise NotImplementedError(mock_msg)

        test_func = self._service.cache.set
        test_args = [get_obj_db] if args == PLURAL else get_obj_db
        self._service.bg_tasks = BackgroundTasks()
        monkeypatch.setattr(BackgroundTasks, 'add_task', mock)
        mock_msg = 'Mocked background_tasks'

        with pytest.raises(NotImplementedError, match=mock_msg):
            await self._service._add_bg_task_or_execute(test_func, test_args)

    async def test_get_returns_None(self) -> None:
        assert await self._db_empty()
        assert await self._cache_empty()
        assert await self._service.get(id=ID) is None

    async def test_get_all_returns_empty_list(self) -> None:
        assert await self._db_empty()
        assert await self._cache_empty()
        assert await self._service.get() == []

    @pytest.mark.parametrize('kwargs', ({}, {'id': ID}))
    async def test_get_raises_not_found_exception(self, kwargs) -> None:
        assert await self._db_empty()
        assert await self._cache_empty()
        with pytest.raises(HTTPException, match=self.get_regex_not_found()):
            await self._service.get(exception=True, **kwargs)  # type: ignore  [attr-defined]

    @pytest.mark.parametrize('method_name', ('refresh', 'get'))
    async def test_get_returns_obj_from_db_and_setup_cache(self, get_obj_db, method_name) -> None:
        assert await self._cache_empty()
        from_db = await self._service.__getattribute__(method_name)(id=get_obj_db.id)
        self.compare_objs(from_db, get_obj_db)
        assert await self._cache_equals_db()

    @pytest.mark.parametrize('method_name', ('refresh', 'get'))
    async def test_get_all_return_objs_from_db_and_setup_cache(self, get_obj_db, method_name) -> None:
        assert await self._cache_empty()
        from_db = await self._service.__getattribute__(method_name)()
        self.compare_objs(from_db[0], get_obj_db)
        assert await self._cache_equals_db()

    async def test_get_returns_obj_from_cache(self, get_obj_cache) -> None:
        assert await self._db_empty()
        from_cache = await self._service.get(id=get_obj_cache.id)  # type: ignore  [attr-defined]
        self.compare_objs(from_cache, get_obj_cache)

    async def test_get_all_return_objs_from_cache(self, get_obj_cache) -> None:
        assert await self._db_empty()
        from_cache = await self._service.get()  # type: ignore  [attr-defined]
        self.compare_objs(from_cache[0], get_obj_cache)

    async def test_create_method(self) -> None:
        assert await self._db_empty()
        assert await self._cache_empty()
        created = await self._service.create(**self.create_data)
        from_db = await self._service.db.get(id=created.id)
        self.compare_obj_data(from_db, self.create_data)
        assert await self._cache_equals_db()

    async def test_update_method(self, get_obj_db) -> None:
        assert await self._cache_empty()
        updated = await self._service.update(id=get_obj_db.id, **self.update_data)
        from_db = await self._service.db.get(id=updated.id)
        self.compare_obj_data(from_db, self.update_data)
        assert await self._cache_equals_db()

    async def test_delete_method(self, get_obj_db) -> None:
        assert not await self._db_empty()
        await self._service.refresh(id=get_obj_db.id)
        assert await self._cache_equals_db()
        await self._service.delete(id=get_obj_db.id)
        assert await self._db_empty()
        assert await self._cache_empty()
