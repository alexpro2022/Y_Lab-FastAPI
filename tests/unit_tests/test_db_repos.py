import pytest
from uuid import uuid4
from fastapi import HTTPException
from sqlalchemy import Row

from app.models import Dish, Menu, Submenu
from app.repositories.db_repository import (CRUDRepository, DishRepository,
                                            MenuRepository, SubmenuRepository)
from tests.unit_tests.base_crud_tests.utils import get_regex_not_found


class TestCRUDRepository:
    @staticmethod
    def test_is_allowed_methods_not_raising_exception() -> None:
        assert CRUDRepository.is_delete_allowed_not_in_use
        assert CRUDRepository.is_update_allowed_not_in_use


class GenericRepoTest:
    def test_repo(self, get_test_session) -> None:
        repo = self.repo(get_test_session)  # type: ignore
        assert isinstance(repo, CRUDRepository)
        assert self.model == repo.model  # type: ignore
        assert self.msg_not_found == repo.msg_not_found  # type: ignore
        assert self.msg_already_exists == repo.msg_already_exists  # type: ignore


class TestSubmenuRepository(GenericRepoTest):
    model = Submenu
    repo = SubmenuRepository
    msg_not_found = 'submenu not found'
    msg_already_exists = 'Подменю с таким заголовком уже существует.'


class TestDishRepository(GenericRepoTest):
    model = Dish
    repo = DishRepository
    msg_not_found = 'dish not found'
    msg_already_exists = 'Блюдо с таким заголовком уже существует.'


class TestMenuRepository(GenericRepoTest):
    model = Menu
    repo = MenuRepository
    msg_not_found = 'menu not found'
    msg_already_exists = 'Меню с таким заголовком уже существует.'

    async def test_get_or_404_raises_exc(self, init_db, menu_repo):
        with pytest.raises(HTTPException, match=get_regex_not_found(self.msg_not_found)):
            await menu_repo.get_or_404_(uuid4())

    async def test_get_all(self, init_db, menu_repo):
        with pytest.raises(HTTPException, match=get_regex_not_found(self.msg_not_found)):
            await menu_repo.get_all_(exception=True)

    def _compare(self, obj: Row, menu: Menu) -> None:
        assert isinstance(obj, Row)
        assert obj.id == menu.id
        assert obj.title == menu.title
        assert obj.description == menu.description
        assert hasattr(obj, 'submenus_count')
        assert hasattr(obj, 'dishes_count')
        assert obj.submenus_count == 0
        assert obj.dishes_count == 0
        return True

    async def test_get_or_404_returns_obj(self, menu, menu_repo) -> None:
        obj = await menu_repo.get_or_404_(menu.id)
        assert self._compare(obj, menu)

    async def test_get_all_returns_list(self, menu, menu_repo) -> None:
        objs = await menu_repo.get_all_()
        assert isinstance(objs, list)
        assert self._compare(objs[0], menu)
