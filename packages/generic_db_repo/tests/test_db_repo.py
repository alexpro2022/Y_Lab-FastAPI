from datetime import datetime as dt
from uuid import uuid4

import pytest
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..generic_db_repository import CRUDBaseRepository, pkType
from .conftest import CRUD, Data, Model, pytest_mark_anyio
from .utils import get_regex, get_regex_not_found


class TestCRUDBaseRepository(Data):
    """Тестовый класс для тестирования базового CRUD класса."""
    msg_already_exists: str = 'Object with such a unique values already exists.'
    msg_not_found: str = 'Object(s) not found.'

    @pytest.fixture(autouse=True)
    def init(self, get_test_session: AsyncSession) -> None:
        # base crud with not implemented hooks
        self.crud_base_not_implemented: CRUDBaseRepository = CRUDBaseRepository(self.model, get_test_session)
        # base crud with bypassed hooks
        self.crud_base_implemented: CRUD = CRUD(self.model, get_test_session)
        self.id_not_found: pkType = 111 if isinstance(self.model.id, int) else uuid4()

    def test_init_fixture(self):
        assert isinstance(self.crud_base_not_implemented, CRUDBaseRepository)
        assert not isinstance(self.crud_base_not_implemented, CRUD)
        assert isinstance(self.crud_base_implemented, CRUD)

    async def _create_object(self) -> Model:
        return await self.crud_base_not_implemented._save(self.model(**self.create_payload))

    def _check_obj(self, obj, after_create: bool = True) -> None:
        assert isinstance(obj, self.model)
        for field_name in self.field_names:
            assert hasattr(obj, field_name)
        payload = self.create_payload if after_create else self.update_payload
        self._compare_values(obj, payload)

    def _compare_values(self, obj: Model, payload: dict[str, str]) -> None:
        assert obj.title == payload['title'], (obj.title, payload['title'])
        assert obj.description == payload['description'], (obj.description, payload['description'])

    async def _db_empty(self):
        return await self.crud_base_not_implemented.get_all() is None

    def test_set_order_by(self):
        assert self.crud_base_not_implemented.set_order_by('') is None

# === CRUD ===
    @pytest_mark_anyio
    async def test_save(self) -> None:
        assert await self._db_empty()
        obj = await self._create_object()
        assert not await self._db_empty()
        self._check_obj(obj)

    @pytest_mark_anyio
    @pytest.mark.parametrize('method_name', ('_get_all_by_attrs', '_get_by_attrs'))
    async def test_get_by_attrs_methods(self, method_name: str) -> None:
        title = self.create_payload['title']
        method = self.crud_base_not_implemented.__getattribute__(method_name)
        # testing return None if NOT_FOUND and exception=False by default
        assert await method(title=title) is None
        # testing raise HTTPException if NOT_FOUND and exception=True
        with pytest.raises(HTTPException, match=get_regex_not_found(self.msg_not_found)):
            await method(title=title, exception=True)
        await self._create_object()
        # testing return list of objects or object if FOUND
        result = await method(title=title)
        obj = result[0] if method_name == '_get_all_by_attrs' else result
        self._check_obj(obj)

    @pytest_mark_anyio
    async def test_get_method(self) -> None:
        """`get` should return None or object."""
        method = self.crud_base_not_implemented.get
        # testing return None
        assert await method(self.id_not_found) is None
        obj = await self._create_object()
        # testing return object
        self._check_obj(await method(pk=obj.id))

    @pytest_mark_anyio
    async def test_get_or_404_method(self) -> None:
        """`get_or_404` should raise `HTTP_404_NOT_FOUND` or return object."""
        method = self.crud_base_not_implemented.get_or_404
        # testing raise HTTP_404_NOT_FOUND
        with pytest.raises(HTTPException, match=get_regex_not_found(self.msg_not_found)):
            await method(self.id_not_found)
        obj = await self._create_object()
        # testing return object
        self._check_obj(await method(pk=obj.id))

    @pytest_mark_anyio
    async def test_get_all_method(self) -> None:
        """`get_all` should raise `HTTP_404_NOT_FOUND` or return "None or object."""
        method = self.crud_base_not_implemented.get_all
        # testing return None
        assert await method() is None
        # testing raise HTTP_404_NOT_FOUND
        with pytest.raises(HTTPException, match=get_regex_not_found(self.msg_not_found)):
            await method(exception=True)
        await self._create_object()
        # testing return list of objects
        objs = await method()
        assert isinstance(objs, list)
        self._check_obj(objs[0])

    # create_update_params: tuple[str, tuple[dict, dict]] = ('kwargs', ({}, {'optional_field': dt.now()}))
    parametrize = pytest.mark.parametrize('kwargs', ({}, {'optional_field': dt.now()}))

    @pytest_mark_anyio
    @parametrize
    # pytest.mark.parametrize(*create_update_params)
    async def test_create_method(self, kwargs) -> None:
        crud = self.crud_base_not_implemented
        assert await self._db_empty()
        obj = await crud.create(self.create_schema(**self.create_payload), **kwargs)
        assert not await self._db_empty()
        created = await crud.get_or_404(obj.id)
        self._check_obj(created)
        assert created.optional_field if kwargs else created.optional_field is None

    @pytest_mark_anyio
    @parametrize
    # pytest.mark.parametrize(*create_update_params)
    async def test_update_method(self, kwargs) -> None:
        crud = self.crud_base_implemented
        obj = await self._create_object()
        self._check_obj(obj)
        await crud.update(obj.id, self.update_schema(**self.update_payload), **kwargs)
        updated = await crud.get_or_404(obj.id)
        self._check_obj(updated, after_create=False)
        assert updated.optional_field if kwargs else updated.optional_field is None

    @pytest_mark_anyio
    async def test_delete_method(self) -> None:
        obj = await self._create_object()
        assert not await self._db_empty()
        await self.crud_base_implemented.delete(obj.id)
        assert await self._db_empty()

# === Exceptions ===
    @pytest_mark_anyio
    async def test_save_method_raises_exception_on_unique(self) -> None:
        await self._create_object()
        with pytest.raises(HTTPException, match=get_regex(self.msg_already_exists, status.HTTP_400_BAD_REQUEST)):
            await self._create_object()

    @pytest.mark.parametrize('method_name, args, expected_msg', (
        ('has_permission', (None, None), 'has_permission() must be implemented.'),
        ('is_update_allowed', (None, None), 'is_update_allowed() must be implemented.'),
        ('is_delete_allowed', (None,), 'is_delete_allowed() must be implemented.'),
    ))
    def test_not_implemented_method_raises_exception(
        self, method_name: str, args: tuple[None, ...], expected_msg: str
    ) -> None:
        with pytest.raises(NotImplementedError, match=get_regex(expected_msg)):
            self.crud_base_not_implemented.__getattribute__(method_name)(*args)

    @pytest_mark_anyio
    @pytest.mark.parametrize('method_name', ('update', 'delete'))
    async def test_update_delete_methods_raise_not_found_exceptions(self, method_name: str) -> None:
        expected_msg = self.msg_not_found
        await self._update_delete_raise_exceptions(method_name, HTTPException, expected_msg, not_found=True)

    @pytest_mark_anyio
    @pytest.mark.parametrize('method_name, expected_msg', (
        ('update', 'is_update_allowed() must be implemented.'),
        ('delete', 'is_delete_allowed() must be implemented.'),
    ))
    async def test_update_delete_methods_raise_is_allowed_exceptions(self, method_name: str, expected_msg: str) -> None:
        await self._update_delete_raise_exceptions(method_name, NotImplementedError, expected_msg, self._create_object)

    @pytest_mark_anyio
    @pytest.mark.parametrize('method_name', ('update', 'delete'))
    async def test_update_delete_methods_raise_has_permission_exception(self, method_name: str) -> None:
        expected_msg = 'has_permission() must be implemented.'
        await self._update_delete_raise_exceptions(
            method_name, NotImplementedError, expected_msg, self._create_object, user=1)

# === Utils ===
    async def _update_delete_raise_exceptions(
        self, method_name, exc_type, expected_msg, func=None, user=None, not_found=False
    ) -> None:
        method = self.crud_base_not_implemented.__getattribute__(method_name)
        idx = self.id_not_found
        if func is not None:
            obj = await func()
            idx = obj.id
        args = (
            (idx,) if method_name == 'delete'
            else (idx, self.update_schema(**self.update_payload))
        )
        regex = get_regex_not_found(self.msg_not_found) if not_found else get_regex(expected_msg)
        with pytest.raises(exc_type, match=regex):
            await method(*args, user=user)
