import pytest
import pytest_asyncio

from app.models import Dish, Menu, Submenu
from app.repositories.db_repository import (CRUD, DishCRUD, MenuCRUD,
                                            SubmenuCRUD)
from packages.generic_db_repo.testing_lib import BaseCRUDTest
from tests.fixtures import data as d


class TestCRUD:
    @staticmethod
    def test_is_allowed_methods_not_raising_exception() -> None:
        assert CRUD.has_permission_not_in_use
        assert CRUD.is_delete_allowed_not_in_use
        assert CRUD.is_update_allowed_not_in_use


class TestMenuCRUD(BaseCRUDTest):
    model = Menu
    crud = MenuCRUD
    msg_not_found = 'menu not found'
    msg_already_exists = 'Меню с таким заголовком уже существует.'
    create_data = d.MENU_POST_PAYLOAD
    update_data = d.MENU_PATCH_PAYLOAD

    @pytest_asyncio.fixture
    async def get_obj(self, menu):
        return menu


class TestSubmenuCRUD(BaseCRUDTest):
    model = Submenu
    crud = SubmenuCRUD
    msg_not_found = 'submenu not found'
    msg_already_exists = 'Подменю с таким заголовком уже существует.'
    create_data = d.SUBMENU_POST_PAYLOAD
    update_data = d.SUBMENU_PATCH_PAYLOAD

    @pytest_asyncio.fixture
    async def get_obj(self, submenu):
        return submenu

    @pytest.fixture
    def get_create_data_extra(self, menu):
        return {'menu_id': menu.id}


class TestDishCRUD(BaseCRUDTest):
    model = Dish
    crud = DishCRUD
    msg_not_found = 'dish not found'
    msg_already_exists = 'Блюдо с таким заголовком уже существует.'
    create_data = d.DISH_POST_PAYLOAD
    update_data = d.DISH_PATCH_PAYLOAD

    @pytest_asyncio.fixture
    async def get_obj(self, dish):
        return dish

    @pytest.fixture
    def get_create_data_extra(self, submenu):
        return {'submenu_id': submenu.id}
