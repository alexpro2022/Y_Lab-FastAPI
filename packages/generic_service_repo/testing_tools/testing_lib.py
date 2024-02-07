import pytest
import pytest_asyncio
from fakeredis import FakeRedis
from fastapi import BackgroundTasks, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from packages.generic_cache_repo.generic_cache_repository import BaseRedis
from packages.generic_db_repo.generic_db_repository import BaseCRUD
from packages.generic_service_repo.generic_service_repository import BaseService

BACKGROUND_TASKS_DATA = ('background_tasks', (None, BackgroundTasks()))
SINGLE_MULTIPLE_DATA = ('args', ('single', 'multiple'))
PK_DATA = ('pk', (None, 1))


class BaseServiceTest:
    msg_not_found = 'Object(s) not found.'
    # msg_not_implemented = "Method or function hasn't been implemented yet."
    service: BaseService
    db: BaseCRUD
    cache: BaseRedis
    create_data: dict

    @pytest_asyncio.fixture(autouse=True)
    async def init(self, get_test_session: AsyncSession, get_test_redis: FakeRedis) -> None:
        self._service = self.service(
            self.db(get_test_session),
            self.cache(get_test_redis),
        )
        # BaseService(CRUD(self.model, get_test_session),
        #                                RedisBaseRepository(get_test_redis))

    def test_init_fixture(self) -> None:
        assert isinstance(self._service, self.service)
        assert isinstance(self._service.db, self.db)
        assert isinstance(self._service.cache, self.cache)
        # assert self.base_service.bg_tasks is None

    '''@pytest_asyncio.fixture()
    async def get_service(self, get_test_session: AsyncSession, get_test_redis: FakeRedis) -> None:
        self.service = Service(CRUD(self.model, get_test_session),
                               RedisBaseRepository(get_test_redis))

    def test_get_service_fixture(self, get_service) -> None:
        assert isinstance(self.service, Service)
        assert isinstance(self.service.db, CRUD)
        assert isinstance(self.service.redis, RedisBaseRepository)
        assert self.service.bg_tasks is None  '''


'''
    @pytest_asyncio.fixture
    async def get_obj_in_db(self) -> Model:
        return await self._service.db.create(self.create_schema(**self.create_payload))

    @pytest_mark_anyio
    async def test_get_obj_in_db_fixture(self, get_obj_in_db) -> None:
        assert not await self._db_empty()
        assert await self._cache_empty()

    async def _db_empty(self) -> bool:
        return await self._service.db.get() is None

    async def _cache_empty(self) -> bool:
        return await self._service.cache.get() is None

    async def _check_cache_equals_db(self) -> None:
        db = await self._service.db.get()
        cache = await self._service.redis.get()
        compare_lists(db, cache)

    @pytest_mark_anyio
    @pytest.mark.parametrize(*SINGLE_MULTIPLE_DATA)
    async def test_set_cache(self, get_test_obj, args) -> None:
        args = [get_test_obj] if args == 'multiple' else get_test_obj
        assert await self._cache_empty()
        await self.base_service.set_cache(args)
        assert not await self._cache_empty()

    @pytest_mark_anyio
    @pytest.mark.parametrize(*PK_DATA)
    async def test__get_returns_None(self, pk) -> None:
        assert await self._db_empty()
        assert await self._cache_empty()
        assert await self.base_service._BaseService__get(pk) is None  # type: ignore  [attr-defined]

    @pytest_mark_anyio
    @pytest.mark.parametrize(*PK_DATA)
    async def test__get_raises_not_found_exception(self, pk) -> None:
        assert await self._db_empty()
        assert await self._cache_empty()
        with pytest.raises(HTTPException) as exc_info:
            await self.base_service._BaseService__get(pk, exception=True)  # type: ignore  [attr-defined]
        check_exception_info_not_found(exc_info, self.msg_not_found)

    @pytest_mark_anyio
    @pytest.mark.parametrize(*PK_DATA)
    async def test__get_returns_obj_from_db_and_setup_cache(self, get_obj_in_db, pk) -> None:
        assert await self._cache_empty()
        result = await self.base_service._BaseService__get(pk)  # type: ignore  [attr-defined]
        obj = result if pk else result[0]
        compare(obj, get_obj_in_db)
        assert not await self._cache_empty()
        await self._check_cache_equals_db()

    @pytest_mark_anyio
    @pytest.mark.parametrize(*PK_DATA)
    async def test__get_returns_obj_from_cache(self, get_test_obj, pk) -> None:
        await self.base_service.set_cache(get_test_obj)
        assert await self._db_empty()
        result = await self.base_service._BaseService__get(pk)  # type: ignore  [attr-defined]
        obj = result if pk else result[0]
        compare(obj, get_test_obj)

    @pytest_mark_anyio
    async def test_get_method(self, get_obj_in_db) -> None:
        """`get` should return None or object."""
        method = self.base_service.get
        assert await method(11) is None  # type: ignore [func-returns-value]
        obj = await method(1)  # type: ignore [func-returns-value]
        compare(obj, get_obj_in_db)

    @pytest_mark_anyio
    async def test_get_or_404_method(self, get_obj_in_db) -> None:
        """`get_or_404` should raise `HTTP_404_NOT_FOUND` or return object."""
        method = self.base_service.get_or_404
        with pytest.raises(HTTPException) as exc_info:
            await method(11)
        check_exception_info_not_found(exc_info, self.msg_not_found)
        obj: Model = await method(1)
        compare(obj, get_obj_in_db)

    @pytest_mark_anyio
    async def test_get_all_method(self) -> None:
        """`get_all` should raise `HTTP_404_NOT_FOUND` or return "None or object."""
        method = self.base_service.get_all
        assert await method() is None
        with pytest.raises(HTTPException) as exc_info:
            await method(exception=True)
        check_exception_info_not_found(exc_info, self.msg_not_found)
        obj = await self.base_service.db.create(self.create_schema(**self.create_payload))
        objs: list[Model] = await method()  # type: ignore [assignment]
        compare(objs[0], obj)

    @pytest_mark_anyio
    @pytest.mark.parametrize(*BACKGROUND_TASKS_DATA)
    @pytest.mark.parametrize(*SINGLE_MULTIPLE_DATA)
    async def test_add_bg_task_or_execute(self, get_test_obj, background_tasks, args) -> None:
        self.base_service.bg_tasks = background_tasks
        args = [get_test_obj] if args == 'multiple' else get_test_obj
        assert await self._cache_empty()
        await self.base_service._add_bg_task_or_execute(self.base_service.set_cache, args)
        if self.base_service.bg_tasks:  # adding the method set_cache to background but cannot run it as it works via DI
            assert await self._cache_empty()
        else:  # executing the method set_cache directly bypassing bg_tasks
            assert not await self._cache_empty()

    @pytest_mark_anyio
    @pytest.mark.parametrize(*BACKGROUND_TASKS_DATA)
    async def test_create_method(self, get_service, background_tasks) -> None:
        self.service.bg_tasks = background_tasks
        assert await self._db_empty()
        assert await self._cache_empty()
        created: Model = await self.service.create(self.create_schema(**self.create_payload))
        assert not await self._db_empty()
        obj = await self.service.db.get_or_404(created.id)
        compare(obj, created)
        if self.service.bg_tasks:
            assert await self._cache_empty()
        else:
            await self._check_cache_equals_db()

    @pytest_mark_anyio
    @pytest.mark.parametrize(*BACKGROUND_TASKS_DATA)
    async def test_update_method(self, get_service, get_obj_in_db, background_tasks) -> None:
        self.service.bg_tasks = background_tasks
        obj = await self.service.db.get_or_404(get_obj_in_db.id)
        compare(obj, get_obj_in_db)
        updated: Model = await self.service.update(get_obj_in_db.id, self.update_schema(**self.update_payload))
        obj = await self.service.db.get_or_404(get_obj_in_db.id)
        compare(updated, obj)
        if self.service.bg_tasks:
            assert await self._cache_empty()
        else:
            await self._check_cache_equals_db()

    @pytest_mark_anyio
    async def test_delete_method(self, get_service) -> None:
        created: Model = await self.service.create(self.create_schema(**self.create_payload))
        assert not await self._db_empty()
        assert not await self._cache_empty()
        await self.service.delete(created.id)
        assert await self._db_empty()
        assert await self._cache_empty()

# === Exceptions ===
    @pytest_mark_anyio
    @pytest.mark.parametrize('method_name', ('update', 'delete', 'get_or_404', 'get_all'))
    async def test_method_raises_exception_not_found(self, method_name) -> None:
        pk = 1
        payload = self.update_schema(**self.update_payload)
        match method_name:
            case 'update':
                args = (pk, payload)
            case 'get_all':
                args = (True, )  # type: ignore [assignment]
            case _:
                args = (pk,)  # type: ignore [assignment]
        with pytest.raises(HTTPException) as exc_info:
            await self.base_service.__getattribute__(method_name)(*args)
        check_exception_info_not_found(exc_info, self.msg_not_found)

    @pytest_mark_anyio
    @pytest.mark.parametrize('method_name', (
        'set_cache_on_create', 'set_cache_on_update', 'set_cache_on_delete', 'create', 'update', 'delete'
    ))
    async def test_method_raises_exception_not_implemented(self, method_name, get_obj_in_db) -> None:
        pk = 1
        payload = self.update_schema(**self.update_payload)
        match method_name:
            case 'update':
                args = (pk, payload)
            case 'create':
                args = (payload,)  # type: ignore [assignment]
            case _:
                args = (pk,)  # type: ignore [assignment]
        with pytest.raises(NotImplementedError) as exc_info:
            await self.base_service.__getattribute__(method_name)(*args)
        check_exception_info(exc_info, self.msg_not_implemented)

    @pytest_mark_anyio
    @pytest.mark.parametrize('method_name', ('create', 'update', 'delete'))
    async def test_method_not_raising_exception_not_implemented_from_bg_task(self, method_name, get_obj_in_db) -> None:
        self.base_service.bg_tasks = BackgroundTasks()
        pk = 1
        payload = self.update_schema(**self.update_payload)
        match method_name:
            case 'update':
                args = (pk, payload)
            case 'create':
                args = (payload,)  # type: ignore [assignment]
            case _:
                args = (pk, )  # type: ignore [assignment]
        # cannot run task from background as it works via DI
        await self.base_service.__getattribute__(method_name)(*args)
'''
