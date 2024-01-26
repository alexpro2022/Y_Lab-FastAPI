from typing import Any, AsyncGenerator

import pytest
import pytest_asyncio
from fastapi import Request, Response  # noqa
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession  # noqa

from app.core import settings  # noqa
from app.main import app
from app.models import Dish, Menu, Submenu  # noqa
from app.repositories.db_repository import DishRepository  # noqa
from app.repositories.db_repository import MenuRepository  # noqa
from app.repositories.db_repository import SubmenuRepository  # noqa
from app.schemas.schemas import MenuIn, MenuOut  # noqa
from packages.generic_db_repo.tests.conftest import *  # noqa
from .fixtures.data import (DISH_POST_PAYLOAD, ENDPOINT_DISH, ENDPOINT_MENU,
                            ENDPOINT_SUBMENU, MENU_POST_PAYLOAD,
                            SUBMENU_POST_PAYLOAD)

# pytest_plugins = [
# 'packages.generic_db_repo.tests.fixture.data'
# 'packages.generic_db_repo.tests.fixture.fixtures']

pytest_mark_anyio = pytest.mark.asyncio
# pytest_mark_anyio = pytest.mark.anyio

'''
engine = create_async_engine('sqlite+aiosqlite:///./test.db',
                             connect_args={'check_same_thread': False})

TestingSessionLocal = async_sessionmaker(expire_on_commit=False,
                                         autocommit=False,
                                         autoflush=False,
                                         bind=engine)
'''


async def override_get_async_session() -> AsyncGenerator[Any, None]:
    async with test_session() as session:
        yield session

app.dependency_overrides[get_async_session] = override_get_async_session


'''
@pytest_asyncio.fixture(autouse=True)
async def init_db() -> AsyncGenerator[None, Any]:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
'''


# --- Fixtures for endpoints testing -----------------------------------------------
@pytest_asyncio.fixture
async def async_client() -> AsyncGenerator[AsyncClient, Any]:
    async with AsyncClient(app=app, base_url='http://test') as ac:
        yield ac


@pytest_asyncio.fixture
async def get_menu_repo(get_test_session) -> AsyncGenerator[MenuRepository, Any]:  # noqa
    yield MenuRepository(get_test_session)


@pytest_asyncio.fixture
async def menu(get_menu_repo: MenuRepository):  # ): async_client: AsyncClient
    created = await get_menu_repo.create(MenuIn(**MENU_POST_PAYLOAD))
    yield created
    # menu = await async_client.post(ENDPOINT_MENU, json=MENU_POST_PAYLOAD)
    # assert menu.status_code == 201, (menu.headers, menu.content)
    # yield menu

'''
@pytest_asyncio.fixture
async def submenu(async_client: AsyncClient, menu: Response) -> Response:
    assert menu.status_code == 201, (menu.headers, menu.content)
    submenu = await async_client.post(ENDPOINT_SUBMENU, json=SUBMENU_POST_PAYLOAD)
    assert submenu.status_code == 201, (submenu.headers, submenu.content)
    yield submenu


@pytest_asyncio.fixture
async def dish(async_client: AsyncClient, submenu: Response) -> Response:
    assert submenu.status_code == 201, (submenu.headers, submenu.content)
    dish = await async_client.post(ENDPOINT_DISH, json=DISH_POST_PAYLOAD)
    assert dish.status_code == 201, (dish.headers, dish.content)
    yield dish
'''

# --- Fixtures for repository testing -----------------------------------------------
'''@pytest_asyncio.fixture
async def get_test_session() -> Generator[Any, Any, None]:
    async with TestingSessionLocal() as session:
        yield session
'''

'''



@pytest_asyncio.fixture
async def get_submenu_repo(get_test_session: AsyncSession) -> Generator[SubmenuRepository, Any, None]:
    yield SubmenuRepository(get_test_session)


@pytest_asyncio.fixture
async def get_dish_repo(get_test_session: AsyncSession) -> Generator[DishRepository, Any, None]:
    yield DishRepository(get_test_session)
'''

'''
@pytest_asyncio.fixture
async def get_test_redis() -> AsyncGenerator[FakeRedis, Any]:
    r = FakeRedis()
    yield r
    await r.flushall()


@pytest_asyncio.fixture
async def get_menu_service(
    get_test_session: AsyncSession, get_test_redis: FakeRedis
) -> Generator[MenuService, Any, None]:
    yield MenuService(get_test_session, get_test_redis, None)


@pytest_asyncio.fixture
async def get_submenu_service(
    get_test_session: AsyncSession, get_test_redis: FakeRedis
) -> Generator[SubmenuService, Any, None]:
    yield SubmenuService(get_test_session, get_test_redis, None)


@pytest_asyncio.fixture
async def get_dish_service(
    get_test_session: AsyncSession, get_test_redis: FakeRedis
) -> Generator[DishService, Any, None]:
    yield DishService(get_test_session, get_test_redis, None)
'''
