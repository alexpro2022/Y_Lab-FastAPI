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


# --- Fixtures for endpoints testing -----------------------------------------------
def test_async_client(async_client) -> None:
    assert isinstance(async_client, AsyncClient)


'''


def test_menu_dynamic(request: c.Request) -> None:
    menu = request.getfixturevalue('menu')
    assert menu.status_code == 201, (menu.headers, menu.content)


def test_submenu(submenu: c.Response) -> None:
    assert submenu.status_code == 201, (submenu.headers, submenu.content)


def test_submenu_dynamic(request: c.Request) -> None:
    submenu = request.getfixturevalue('submenu')
    assert submenu.status_code == 201, (submenu.headers, submenu.content)


def test_dish(dish: c.Response) -> None:
    assert dish.status_code == 201, (dish.headers, dish.content)


def test_dish_dynamic(request: c.Request) -> None:
    dish = request.getfixturevalue('dish')
    assert dish.status_code == 201, (dish.headers, dish.content)
'''

'''
# --- Fixtures for repository testing -----------------------------------------------
@c.pytest_mark_anyio
async def test_get_test_redis(get_test_redis: c.FakeRedis) -> None:
    assert isinstance(get_test_redis, c.FakeRedis)
    assert await get_test_redis.set('key', 'value')
    assert await get_test_redis.get('key') == b'value'
    assert await get_test_redis.set('key', 'value2')
    assert await get_test_redis.get('key') == b'value2'
    assert await get_test_redis.delete('key')
    assert await get_test_redis.get('key') is None





def test_get_menu_service(get_menu_service: c.MenuService) -> None:
    assert isinstance(get_menu_service, c.MenuService)


def test_get_submenu_repo(get_submenu_repo: c.SubmenuRepository) -> None:
    assert isinstance(get_submenu_repo, c.SubmenuRepository)


def test_get_submenu_service(get_submenu_service: c.SubmenuService) -> None:
    assert isinstance(get_submenu_service, c.SubmenuService)


def test_get_dish_repo(get_dish_repo: c.DishRepository) -> None:
    assert isinstance(get_dish_repo, c.DishRepository)


def test_get_dish_service(get_dish_service: c.DishService) -> None:
    assert isinstance(get_dish_service, c.DishService)
'''
