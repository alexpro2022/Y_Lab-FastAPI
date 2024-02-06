from typing import TypeAlias
from uuid import UUID

from tests.fixtures import data as d

Json: TypeAlias = dict[str, str | int]


def _check_response(response_json: Json | list[Json], expected_result: Json | list[Json]) -> str:
    assert type(response_json) is type(expected_result)
    if isinstance(response_json, list):
        response_json, expected_result = response_json[0], expected_result[0]
    try:
        UUID(str(response_json.pop('id')))
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
