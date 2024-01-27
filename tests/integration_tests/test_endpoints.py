import pytest
from fastapi import status
from httpx import AsyncClient

from app.models import Dish, Menu, Submenu
from app.repositories.db_repository import (DishRepository, MenuRepository,
                                            SubmenuRepository)
from packages.endpoint_testing_lib.endpoint_testing_lib import (
    not_allowed_methods_test, standard_tests)
from tests.conftest import pytest_mark_anyio
from tests.fixtures import data as d
from tests.integration_tests import utils as u

DELETE, GET, POST, PUT, PATCH = 'DELETE', 'GET', 'POST', 'PUT', 'PATCH'
DOUBLE_NONE = (None, None)

pytestmark = pytest_mark_anyio


@pytest.mark.parametrize('endpoint', (d.ENDPOINT_DISH, d.ENDPOINT_MENU, d.ENDPOINT_SUBMENU))
async def test_not_allowed_method(async_client: AsyncClient, endpoint: str) -> None:
    await not_allowed_methods_test(async_client, (PUT,), endpoint)


@pytest.mark.parametrize('endpoint', (
    d.ENDPOINT_DISH_DEFAULT, d.ENDPOINT_MENU, d.ENDPOINT_SUBMENU_DEFAULT
))
async def test_get_all_returns_empty_list(async_client: AsyncClient, endpoint: str) -> None:
    response = await async_client.get(endpoint)
    assert response.status_code == status.HTTP_200_OK, response.json()
    assert response.json() == []


async def test_menu_post(async_client: AsyncClient, menu_repo: MenuRepository) -> None:
    assert not await menu_repo.get_all()
    await standard_tests(async_client, POST, d.ENDPOINT_MENU,
                         json=d.MENU_POST_PAYLOAD,
                         msg_already_exists=d.MENU_ALREADY_EXISTS_MSG,
                         msg_not_found=d.MENU_NOT_FOUND_MSG,
                         func_check_valid_response=u.check_created_menu)
    assert await menu_repo.get_all()


async def test_submenu_post(
        menu: Menu, async_client: AsyncClient, submenu_repo: SubmenuRepository) -> None:
    assert not await submenu_repo.get_all()
    await standard_tests(async_client, POST, d.ENDPOINT_SUBMENU.format(id=menu.id),
                         json=d.SUBMENU_POST_PAYLOAD,
                         msg_already_exists=d.SUBMENU_ALREADY_EXISTS_MSG,
                         msg_not_found=d.SUBMENU_NOT_FOUND_MSG,
                         func_check_valid_response=u.check_created_submenu)
    assert await submenu_repo.get_all()


async def test_dish_post(
        submenu: Submenu, async_client: AsyncClient, dish_repo: DishRepository) -> None:
    assert not await dish_repo.get_all()
    await standard_tests(async_client, POST, d.ENDPOINT_DISH.format(id=submenu.id),
                         json=d.DISH_POST_PAYLOAD,
                         msg_already_exists=d.DISH_ALREADY_EXISTS_MSG,
                         msg_not_found=d.DISH_NOT_FOUND_MSG,
                         func_check_valid_response=u.check_dish)
    assert await dish_repo.get_all()


@pytest.mark.parametrize('method, endpoint, payload, msg_already_exists, msg_not_found, check_func', (
    (GET, d.ENDPOINT_MENU, None, *d.MENU_MSG_PACK, u.check_menu_list),
    (GET, d.ENDPOINT_MENU, None, *d.MENU_MSG_PACK, u.check_menu),
    (PATCH, d.ENDPOINT_MENU, d.MENU_PATCH_PAYLOAD, *d.MENU_MSG_PACK, u.check_menu_updated),
    (DELETE, d.ENDPOINT_MENU, None, *d.MENU_MSG_PACK, u.check_menu_deleted),
    # -------------------------------------------------------------------------------------------------
    (GET, d.ENDPOINT_SUBMENU, None, *d.SUBMENU_MSG_PACK, u.check_submenu_list),
    (GET, d.ENDPOINT_SUBMENU, None, *d.SUBMENU_MSG_PACK, u.check_submenu),
    (PATCH, d.ENDPOINT_SUBMENU, d.SUBMENU_PATCH_PAYLOAD, *d.SUBMENU_MSG_PACK, u.check_submenu_updated),
    (DELETE, d.ENDPOINT_SUBMENU, None, *d.SUBMENU_MSG_PACK, u.check_submenu_deleted),
    # -------------------------------------------------------------------------------------------------
    (GET, d.ENDPOINT_DISH, None, *d.DISH_MSG_PACK, u.check_dish_list),
    (GET, d.ENDPOINT_DISH, None, *d.DISH_MSG_PACK, u.check_dish),
    (PATCH, d.ENDPOINT_DISH, d.DISH_PATCH_PAYLOAD, *d.DISH_MSG_PACK, u.check_dish_updated),
    (DELETE, d.ENDPOINT_DISH, None, *d.DISH_MSG_PACK, u.check_dish_deleted),
))
async def test_standard(dish: Dish,
                        async_client: AsyncClient,
                        menu_repo: MenuRepository,
                        submenu_repo: SubmenuRepository,
                        dish_repo: DishRepository,
                        method: str,
                        endpoint: str,
                        payload: str,
                        msg_already_exists: str,
                        msg_not_found: str,
                        check_func) -> None:
    repo, obj, parent = await u.prepare(
        endpoint, dish=dish, menu_repo=menu_repo, submenu_repo=submenu_repo, dish_repo=dish_repo
    )
    assert len(await repo.get_all()) == 1
    await standard_tests(async_client,
                         method,
                         endpoint=u.get_endpoint(endpoint, parent),
                         path_param=None if 'list' in check_func.__name__ else obj.id,
                         json=payload,
                         msg_already_exists=msg_already_exists,
                         msg_not_found=msg_not_found,
                         func_check_valid_response=check_func)
    if method == DELETE:
        assert not await repo.get_all()
    else:
        assert len(await repo.get_all()) == 1
