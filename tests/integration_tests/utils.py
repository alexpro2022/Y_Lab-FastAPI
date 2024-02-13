from http import HTTPStatus
from typing import Any, Callable, TypeAlias
from uuid import UUID

import pytest
from httpx import AsyncClient

from packages.generic_api.testing_lib import GenericAPITests
from tests.fixtures import data as d

Json: TypeAlias = dict[str, Any]
callable: TypeAlias = Callable[[Json], str]


class AppGenericAPITests(GenericAPITests):

    @pytest.fixture(autouse=True)
    def mock_dish_discount_(self, mock_dish_discount):
        pass


def _check_response(response_json: Json | list[Json], expected_result: Json | list[Json]) -> str:
    assert type(response_json) is type(expected_result)
    if isinstance(response_json, list) and isinstance(expected_result, list):
        response_json, expected_result = response_json[0], expected_result[0]
    try:
        UUID(str(response_json.pop('id')))  # type:ignore [arg-type]
    except ValueError:
        raise AssertionError('Primary key is not uuid type')
    except KeyError:
        pass
    assert isinstance(response_json, dict)
    assert isinstance(expected_result, dict)
    assert response_json.items() == expected_result.items()
    return 'DONE'


def check_menu_created(response_json: Json) -> str:
    return _check_response(response_json, d.CREATED_MENU)


def check_submenu_created(response_json: Json) -> str:
    return _check_response(response_json, d.CREATED_SUBMENU)


def check_dish(response_json: Json) -> str:
    return _check_response(response_json, d.CREATED_DISH)


def check_dish_updated(response_json: Json) -> str:
    return _check_response(response_json, d.UPDATED_DISH)


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


async def del_dish(async_client: AsyncClient, submenu_id: str, dish_id: str) -> None:
    endpoint = f'{d.ENDPOINT_DISH.format(id=submenu_id)}/{dish_id}'
    await _del(async_client, endpoint, 'dish')


async def del_submenu(async_client: AsyncClient, menu_id: str, submenu_id: str) -> None:
    endpoint = f'{d.ENDPOINT_SUBMENU.format(id=menu_id)}/{submenu_id}'
    await _del(async_client, endpoint, 'submenu')


async def del_menu(async_client: AsyncClient, menu_id: str) -> None:
    endpoint = f'{d.ENDPOINT_MENU}/{menu_id}'
    await _del(async_client, endpoint, 'menu')
