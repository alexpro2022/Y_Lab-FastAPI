import asyncio

from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Dish, Menu, Submenu
from app.repositories.db_repository import (DishRepository, MenuRepository,
                                            SubmenuRepository)


async def test_provided_loop_is_running_loop(event_loop) -> None:
    assert event_loop is asyncio.get_running_loop()


def test_get_test_session(get_test_session) -> None:
    assert isinstance(get_test_session, AsyncSession)


def test_async_client(async_client) -> None:
    assert isinstance(async_client, AsyncClient)


def test_menu_repo(menu_repo) -> None:
    assert isinstance(menu_repo, MenuRepository)


def test_submenu_repo(submenu_repo) -> None:
    assert isinstance(submenu_repo, SubmenuRepository)


def test_dish_repo(dish_repo) -> None:
    assert isinstance(dish_repo, DishRepository)


def test_menu(menu) -> None:
    assert isinstance(menu, Menu)


def test_submenu(submenu) -> None:
    assert isinstance(submenu, Submenu)


def test_dish(dish) -> None:
    assert isinstance(dish, Dish)
