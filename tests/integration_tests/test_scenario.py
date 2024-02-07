from http import HTTPStatus
from typing import Callable, TypeAlias

from httpx import AsyncClient

from tests.fixtures import data as d
from tests.integration_tests.utils import (
    Json,
    check_dish,
    check_dish_updated,
    check_menu_created,
    check_submenu_created,
)

callable: TypeAlias = Callable[[Json], str]


def _check_obj(response_json: Json, check_func: callable | None = None) -> None:
    assert response_json.get('id') is not None
    if check_func is not None:
        assert check_func(response_json) == 'DONE'


# --- POST ---
async def _post(async_client: AsyncClient, endpoint: str, json: Json, check_func: callable) -> Json:
    response = await async_client.post(endpoint, json=json)
    assert response.status_code == HTTPStatus.CREATED
    _check_obj(response.json(), check_func)
    return response.json()


async def post_menu(async_client: AsyncClient,
                    json: Json = d.MENU_POST_PAYLOAD,
                    check_func: callable = check_menu_created) -> Json:
    return await _post(async_client, d.ENDPOINT_MENU, json, check_func)


async def post_submenu(async_client: AsyncClient, menu_id: str,
                       json: Json = d.SUBMENU_POST_PAYLOAD,
                       check_func: callable = check_submenu_created) -> Json:
    return await _post(async_client, d.ENDPOINT_SUBMENU.format(id=menu_id), json, check_func)


async def post_dish(async_client: AsyncClient, menu_id: str, submenu_id: str,
                    json: Json = d.DISH_POST_PAYLOAD,
                    check_func: callable = check_dish) -> Json:
    return await _post(async_client, d.ENDPOINT_DISH.format(id=submenu_id), json, check_func)


# --- GET ---
async def _get(async_client: AsyncClient, endpoint: str) -> Json | list[Json]:
    response = await async_client.get(endpoint)
    assert response.status_code == HTTPStatus.OK
    response_json = response.json()
    if response_json:  # not empty list
        if isinstance(response_json, list):
            response_json = response_json[0]
        _check_obj(response_json)
    return response.json()


async def get_menu(async_client: AsyncClient, menu_id: str,
                   submenus_count: int = 0, dishes_count: int = 0) -> None:
    endpoint = f'{d.ENDPOINT_MENU}/{menu_id}'
    response = await _get(async_client, endpoint)
    assert isinstance(response, dict)
    assert response['submenus_count'] == submenus_count
    assert response['dishes_count'] == dishes_count


async def get_submenu(async_client: AsyncClient,
                      menu_id: str, submenu_id: str,
                      dishes_count: int = 0) -> None:
    endpoint = f'{d.ENDPOINT_SUBMENU.format(id=menu_id)}/{submenu_id}'
    response = await _get(async_client, endpoint)
    assert isinstance(response, dict)
    assert response['dishes_count'] == dishes_count


# --- LIST ---
async def _get_all(async_client: AsyncClient, endpoint: str, expected_result: list[Json]) -> None:
    response = await _get(async_client, endpoint)
    assert response == expected_result


async def get_menus(async_client: AsyncClient, expected_result: list[Json]) -> None:
    await _get_all(async_client, d.ENDPOINT_MENU, expected_result)


async def get_submenus(async_client: AsyncClient, menu_id: str, expected_result: list[Json]) -> None:
    await _get_all(async_client, d.ENDPOINT_SUBMENU.format(id=menu_id), expected_result)


async def get_dishes(async_client: AsyncClient, menu_id: str, submenu_id: str, expected_result: list[Json]) -> None:
    await _get_all(async_client, d.ENDPOINT_DISH.format(id=submenu_id), expected_result)


# --- DELETE ---
async def _del(async_client: AsyncClient, endpoint: str, item_name: str) -> None:
    response = await async_client.delete(endpoint)
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'status': True, 'message': f'The {item_name} has been deleted'}


async def del_submenu(async_client: AsyncClient, menu_id: str, submenu_id: str) -> None:
    endpoint = f'{d.ENDPOINT_SUBMENU.format(id=menu_id)}/{submenu_id}'
    await _del(async_client, endpoint, 'submenu')


async def del_menu(async_client: AsyncClient, menu_id: str) -> None:
    endpoint = f'{d.ENDPOINT_MENU}/{menu_id}'
    await _del(async_client, endpoint, 'menu')


# === TEST SCENARIO ===
async def test_scenario(init_db, async_client: AsyncClient) -> None:
    menu: Json = await post_menu(async_client)
    menu_id = menu['id']
    submenu: Json = await post_submenu(async_client, menu_id)
    submenu_id = submenu['id']
    await post_dish(async_client, menu_id, submenu_id)
    await post_dish(  # must use different payload as the title is unique, so check_func also different
        async_client, menu_id, submenu_id, d.DISH_PATCH_PAYLOAD, check_dish_updated)
    assert 0
    await get_menu(async_client, menu_id, submenus_count=1, dishes_count=2)
    await get_submenu(async_client, menu_id, submenu_id, dishes_count=2)
    await del_submenu(async_client, menu_id, submenu_id)
    await get_submenus(async_client, menu_id, [])
    await get_dishes(async_client, menu_id, submenu_id, [])
    await get_menu(async_client, menu_id)
    await del_menu(async_client, menu_id)
    await get_menus(async_client, [])
