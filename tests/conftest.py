from typing import Any, AsyncGenerator

import pytest

from app.main import app
from packages.generic_db_repo.dependencies import get_async_session
from packages.generic_db_repo.tests.fixture.fixtures import test_session

pytest_plugins = [
    'tests.fixtures.data',
    'tests.fixtures.fixtures',
]

pytest_mark_anyio = pytest.mark.asyncio
# pytest_mark_anyio = pytest.mark.anyio


async def override_get_async_session() -> AsyncGenerator[Any, None]:
    async with test_session() as session:
        yield session

app.dependency_overrides[get_async_session] = override_get_async_session


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


'''




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
'''
engine = create_async_engine('sqlite+aiosqlite:///./test.db',
                             connect_args={'check_same_thread': False})

TestingSessionLocal = async_sessionmaker(expire_on_commit=False,
                                         autocommit=False,
                                         autoflush=False,
                                         bind=engine)
'''
'''
@pytest_asyncio.fixture(autouse=True)
async def init_db() -> AsyncGenerator[None, Any]:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
'''
