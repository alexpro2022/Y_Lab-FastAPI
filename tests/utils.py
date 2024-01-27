import typing

from deepdiff import DeepDiff

from app.repositories.db_repository import (DishRepository, MenuRepository,
                                            SubmenuRepository)
from packages.endpoint_testing_lib.utils import DONE
from packages.generic_db_repo.base import Base
from tests.fixtures import data as d


def _check_response(response_json: dict | list, expected_result: dict | list[dict]) -> str:
    assert response_json == expected_result
    return DONE


def check_created_menu(response_json: dict) -> str:
    return _check_response(response_json, d.CREATED_MENU)


def check_menu(response_json: list) -> str:
    return _check_response(response_json, d.EXPECTED_MENU)


def check_menu_list(response_json: list) -> str:
    return _check_response(response_json, [d.EXPECTED_MENU])


def check_menu_updated(response_json: dict) -> str:
    return _check_response(response_json, d.UPDATED_MENU)


def check_menu_deleted(response_json: dict) -> str:
    return _check_response(response_json, d.DELETED_MENU)


def check_created_submenu(response_json: dict) -> str:
    return _check_response(response_json, d.CREATED_SUBMENU)


def check_submenu(response_json: list) -> str:
    return _check_response(response_json, d.EXPECTED_SUBMENU)


def check_submenu_list(response_json: list) -> str:
    return _check_response(response_json, [d.EXPECTED_SUBMENU])


def check_submenu_updated(response_json: dict) -> str:
    return _check_response(response_json, d.UPDATED_SUBMENU)


def check_submenu_deleted(response_json: dict) -> str:
    return _check_response(response_json, d.DELETED_SUBMENU)


def check_dish(response_json: dict) -> str:
    return _check_response(response_json, d.CREATED_DISH)


def check_dish_list(response_json: list) -> str:
    return _check_response(response_json, [d.CREATED_DISH])


def check_dish_updated(response_json: dict) -> str:
    return _check_response(response_json, d.UPDATED_DISH)


def check_dish_deleted(response_json: dict) -> str:
    return _check_response(response_json, d.DELETED_DISH)


def get_crud(endpoint, *,
             menu_repo: MenuRepository,
             submenu_repo: SubmenuRepository,
             dish_repo: DishRepository
             ) -> MenuRepository | SubmenuRepository | DishRepository:
    res = endpoint.split('/')
    if 'dishes' in res:
        return dish_repo
    elif 'submenus' in res:
        return submenu_repo
    return menu_repo


def compare(left: Base, right: Base) -> None:
    def _get_attrs(item) -> dict[str, typing.Any]:
        assert item
        item_attrs = vars(item)  # .__dict__
        try:
            item_attrs.pop('_sa_instance_state')
        except KeyError:
            pass
        return item_attrs

    diff = DeepDiff(_get_attrs(left), _get_attrs(right), ignore_order=True)
    assert not diff, diff


def compare_lists(left: list[Base], right: list[Base]) -> None:
    assert left
    assert right
    size_left = len(left)
    assert size_left == len(right)
    for i in range(size_left):
        compare(left[i], right[i])
