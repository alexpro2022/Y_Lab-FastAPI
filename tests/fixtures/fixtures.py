from httpx import AsyncClient

from app.main import app
from app.repositories.db_repository import (DishRepository, MenuRepository,
                                            SubmenuRepository)
from app.schemas.schemas import DishIn, MenuIn, SubmenuIn
from packages.generic_db_repo.tests.fixture.fixtures import *  # noqa

from .data import DISH_POST_PAYLOAD, MENU_POST_PAYLOAD, SUBMENU_POST_PAYLOAD


# --- Fixtures for endpoints testing -----------------------------------------------
@pytest_asyncio.fixture
async def async_client() -> AsyncGenerator[AsyncClient, Any]:
    async with AsyncClient(app=app, base_url='http://test') as ac:
        yield ac


@pytest_asyncio.fixture
async def menu_repo(get_test_session) -> AsyncGenerator[MenuRepository, Any]:
    yield MenuRepository(get_test_session)


@pytest_asyncio.fixture
async def submenu_repo(get_test_session) -> AsyncGenerator[SubmenuRepository, Any]:
    yield SubmenuRepository(get_test_session)


@pytest_asyncio.fixture
async def dish_repo(get_test_session) -> AsyncGenerator[DishRepository, Any]:
    yield DishRepository(get_test_session)


@pytest_asyncio.fixture
async def menu(menu_repo):
    created = await menu_repo.create(MenuIn(**MENU_POST_PAYLOAD))
    yield created


@pytest_asyncio.fixture
async def submenu(submenu_repo, menu):
    created = await submenu_repo.create(SubmenuIn(**SUBMENU_POST_PAYLOAD), menu_id=menu.id)
    yield created


@pytest_asyncio.fixture
async def dish(dish_repo, submenu):  # ): async_client: AsyncClient
    created = await dish_repo.create(DishIn(**DISH_POST_PAYLOAD), submenu_id=submenu.id)
    yield created
