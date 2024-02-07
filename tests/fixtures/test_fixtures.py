import asyncio
from typing import Any, AsyncGenerator

from fakeredis.aioredis import FakeRedis
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Dish, Menu, Submenu
from app.repositories.db_repository import DishCRUD, MenuCRUD, SubmenuCRUD


async def test_provided_loop_is_running_loop(event_loop: asyncio.AbstractEventLoop) -> None:
    assert event_loop is asyncio.get_running_loop()


def test_init_db_fixture(init_db: AsyncGenerator) -> None:
    assert init_db is None


def test_get_test_session(get_test_session: AsyncSession) -> None:
    assert isinstance(get_test_session, AsyncSession)


def test_async_client(async_client: AsyncGenerator[AsyncClient, Any]) -> None:
    assert isinstance(async_client, AsyncClient)


def test_menu_repo(menu_repo: MenuCRUD) -> None:
    assert isinstance(menu_repo, MenuCRUD)


def test_submenu_repo(submenu_repo: SubmenuCRUD) -> None:
    assert isinstance(submenu_repo, SubmenuCRUD)


def test_dish_repo(dish_repo: DishCRUD) -> None:
    assert isinstance(dish_repo, DishCRUD)


def test_menu(menu: Menu) -> None:
    assert isinstance(menu, Menu)


def test_submenu(submenu: Submenu) -> None:
    assert isinstance(submenu, Submenu)


def test_dish(dish: Dish) -> None:
    assert isinstance(dish, Dish)


async def test_get_test_redis_fixture(get_test_redis: FakeRedis) -> None:
    assert isinstance(get_test_redis, FakeRedis)
    assert await get_test_redis.get('key') is None
    for value in ('str', 1, 2.2):
        assert await get_test_redis.set('key', value)
        cache = await get_test_redis.get('key')
        assert cache.decode('utf-8') == str(value)
    assert await get_test_redis.delete('key')
    assert await get_test_redis.get('key') is None
