from typing import Any, AsyncGenerator

import pytest
import pytest_asyncio
from httpx import AsyncClient

from app.main import app
from app.models import Dish, Menu, Submenu
from app.repositories.db_repository import DishCRUD, MenuCRUD, SubmenuCRUD
from packages.generic_cache_repo.testing_tools.fixtures import get_test_redis  # noqa
from packages.generic_db_repo.testing_tools.fixtures import (  # noqa
    get_test_session,
    init_db,
)
from tests.fixtures.data import (
    DISH_POST_PAYLOAD,
    MENU_POST_PAYLOAD,
    SUBMENU_POST_PAYLOAD,
)


@pytest_asyncio.fixture(scope='session')
async def async_client() -> AsyncGenerator[AsyncClient, Any]:
    async with AsyncClient(app=app, base_url='http://test') as ac:
        yield ac


@pytest.fixture
def menu_repo(get_test_session) -> MenuCRUD:  # noqa
    return MenuCRUD(get_test_session)


@pytest.fixture
def submenu_repo(get_test_session) -> SubmenuCRUD:  # noqa
    return SubmenuCRUD(get_test_session)


@pytest.fixture
def dish_repo(get_test_session) -> DishCRUD:  # noqa
    return DishCRUD(get_test_session)


@pytest_asyncio.fixture
async def menu(init_db, menu_repo: MenuCRUD) -> Menu:  # noqa
    return await menu_repo.create(**MENU_POST_PAYLOAD)


@pytest_asyncio.fixture
async def submenu(menu, submenu_repo: SubmenuCRUD) -> Submenu:
    return await submenu_repo.create(**SUBMENU_POST_PAYLOAD, menu_id=menu.id)


@pytest_asyncio.fixture
async def dish(submenu, dish_repo: DishCRUD) -> Dish:
    return await dish_repo.create(**DISH_POST_PAYLOAD, submenu_id=submenu.id)
