import re
from typing import Any, Generic
from uuid import uuid4

import pytest
import pytest_asyncio
from fastapi import HTTPException, status
from sqlalchemy import Row
from sqlalchemy.ext.asyncio import AsyncSession

from ..types import ModelType, RepoType, _RepoType


class BaseCRUDTest(Generic[_RepoType]):
    """Тестирование базового CRUD класса."""
    msg_already_exists: str = 'Object with such a unique values already exists.'
    msg_not_found: str = 'Object(s) not found.'
    model: ModelType
    crud: RepoType
    create_data: dict
    create_data_extra: dict
    update_data: dict

# --- Fixtures ---
    @pytest.fixture(autouse=True)
    def init(self, init_db, get_test_session: AsyncSession) -> None:
        self._crud = self.crud(get_test_session)

    def test_init_fixture(self) -> None:
        assert isinstance(self._crud, self.crud)

    @pytest_asyncio.fixture
    async def get_obj(self) -> None:
        """Override the fixture for getting the object from another fixture."""
        return await self._crud._save(self._crud.model(**self.create_data))

    def test_get_obj_fixture(self, get_obj) -> None:
        self._compare(get_obj, self.create_data)

    @pytest.fixture
    def get_create_data_extra(self) -> dict[str, Any]:
        """Returns arbitrary extra data for object creation (like FK of parent entity)."""
        return {}

    def test_get_create_data_extra_fixture(self, get_create_data_extra) -> None:
        assert isinstance(get_create_data_extra, dict)

# --- Testing BaseCRUD ---
    @pytest.mark.parametrize('attr_name, error_msg, class_', (
        ('create_data', 'Class attribute `create_data` must be implemented.', dict),
        ('update_data', 'Class attribute `update_data` must be implemented.', dict),
        ('crud', 'Class attribute `crud` must be implemented.', None),
        ('model', 'Class attribute `model` must be implemented.', None),
    ))
    def test_self_required_attributes(self, attr_name, error_msg, class_) -> None:
        assert hasattr(self, attr_name), error_msg
        if class_ is not None:
            assert isinstance(getattr(self, attr_name), class_)

    def test_messages(self) -> None:
        assert self.msg_already_exists == self.crud.msg_already_exists
        assert self.msg_not_found == self.crud.msg_not_found

    def test_model(self) -> None:
        assert self.model == self._crud.model

    async def test_get_method_returns_none(self) -> None:
        assert await self._crud.get(id=uuid4()) is None

    async def test_get_all_method_returns_empty_list(self) -> None:
        assert await self._crud.get() == []

    async def test_get_method_raises_not_found_exc(self) -> None:
        with pytest.raises(HTTPException, match=self.get_regex_not_found()):
            await self._crud.get(id=uuid4(), exception=True)

    async def test_get_all_method_raises_not_found_exc(self) -> None:
        with pytest.raises(HTTPException, match=self.get_regex_not_found()):
            await self._crud.get(exception=True)

    async def test_get_method_returns_obj(self, get_obj) -> None:
        obj = await self._crud.get(id=get_obj.id)
        self._compare(obj, self.create_data)

    async def test_get_all_method_returns_list(self, get_obj) -> None:
        obj = await self._crud.get()
        assert isinstance(obj, list)
        self._compare(obj[0], self.create_data)

    async def test_create_method(self, get_create_data_extra) -> None:
        data = {**self.create_data, **get_create_data_extra}
        created = await self._crud.create(**data)
        obj = await self._crud.get(id=created.id)
        self._compare(obj, data)

    async def test_unique_constraint(self, get_obj, get_create_data_extra) -> None:
        with pytest.raises(HTTPException, match=self.get_regex_already_exists()):
            await self._crud.create(**self.create_data, **get_create_data_extra)

    async def test_update_method_raises_not_found_exceptions(self) -> None:
        with pytest.raises(HTTPException, match=self.get_regex_not_found()):
            await self._crud.update(id=uuid4(), **self.update_data)

    async def test_update_method(self, get_obj) -> None:
        updated = await self._crud.update(id=get_obj.id, **self.update_data)
        obj = await self._crud.get(id=updated.id)
        self._compare(obj, self.update_data)

    async def test_delete_raises_not_found_exceptions(self) -> None:
        with pytest.raises(HTTPException, match=self.get_regex_not_found()):
            await self._crud.delete(id=uuid4())

    async def test_delete_method(self, get_obj) -> None:
        await self._crud.delete(id=get_obj.id)
        with pytest.raises(HTTPException, match=self.get_regex_not_found()):
            await self._crud.delete(id=get_obj.id)

# --- Utils ---
    @staticmethod
    def get_regex(expected_msg: str, expected_error_code: int | None = None) -> str:
        error_code = '' if expected_error_code is None else f'{expected_error_code}: '
        return re.escape(f'{error_code}{expected_msg}')

    def get_regex_already_exists(self) -> str:
        return self.get_regex(self.msg_already_exists, status.HTTP_400_BAD_REQUEST)

    def get_regex_not_found(self) -> str:
        return self.get_regex(self.msg_not_found, status.HTTP_404_NOT_FOUND)

    def _compare(self, obj, data: dict) -> None:
        assert isinstance(obj, self._crud.model) or isinstance(obj, Row)
        for key in data:
            assert getattr(obj, key) == data[key]
