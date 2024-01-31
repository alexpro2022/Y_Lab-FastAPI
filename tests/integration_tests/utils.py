from uuid import UUID

from tests.integration_tests import data as d


def _check_response(response_json: dict | list[dict], expected_result: dict | list[dict]) -> str:
    assert type(response_json) is type(expected_result)
    if isinstance(response_json, list):
        response_json = response_json[0]
        expected_result = expected_result[0]
    try:
        UUID(str(response_json.pop('id')))
    except ValueError:
        raise AssertionError('Primary key is not uuid type')
    except KeyError:
        pass
    assert response_json.items() == expected_result.items()
    return 'DONE'


def check_menu_created(response_json: dict) -> str:
    return _check_response(response_json, d.CREATED_MENU)


def check_submenu_created(response_json: dict) -> str:
    return _check_response(response_json, d.CREATED_SUBMENU)


def check_dish(response_json: dict) -> str:
    return _check_response(response_json, d.CREATED_DISH)


def check_dish_updated(response_json: dict) -> str:
    return _check_response(response_json, d.UPDATED_DISH)
