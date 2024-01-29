from httpx import AsyncClient
import pytest
from app.main import app
from app.models import Dish, Menu, Submenu
from app.repositories.db_repository import (DishRepository, MenuRepository,
                                            SubmenuRepository)
from app.schemas.schemas import DishIn, MenuIn, SubmenuIn
from packages.generic_db_repo.tests.fixture.fixtures import *  # noqa

from .data import DISH_POST_PAYLOAD, MENU_POST_PAYLOAD, SUBMENU_POST_PAYLOAD


@pytest_asyncio.fixture
async def async_client() -> AsyncGenerator[AsyncClient, Any]:
    async with AsyncClient(app=app, base_url='http://test') as ac:
        yield ac


@pytest.fixture
def menu_repo(get_test_session) -> MenuRepository:
    return MenuRepository(get_test_session)


@pytest.fixture
def submenu_repo(get_test_session) -> SubmenuRepository:
    return SubmenuRepository(get_test_session)


@pytest.fixture
def dish_repo(get_test_session) -> DishRepository:
    return DishRepository(get_test_session)


@pytest_asyncio.fixture
async def menu(menu_repo) -> Menu:
    return await menu_repo.create(MenuIn(**MENU_POST_PAYLOAD))


@pytest_asyncio.fixture
async def submenu(submenu_repo, menu) -> Submenu:
    return await submenu_repo.create(SubmenuIn(**SUBMENU_POST_PAYLOAD), menu_id=menu.id)


@pytest_asyncio.fixture
async def dish(dish_repo, submenu) -> Dish:
    return await dish_repo.create(DishIn(**DISH_POST_PAYLOAD), submenu_id=submenu.id)
