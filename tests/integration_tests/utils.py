import typing
from uuid import UUID

from deepdiff import DeepDiff

from app.repositories.db_repository import (Dish, DishRepository,
                                            MenuRepository, SubmenuRepository)
from packages.endpoint_testing_lib.utils import DONE
from packages.generic_db_repo.base import Base
from tests.fixtures import data as d


def _check_response(response_json: dict | list, expected_result: dict | list[dict]) -> str:
    item = response_json[0] if isinstance(response_json, list) else response_json
    try:
        UUID(str(item.pop('id')))
    except ValueError:
        raise AssertionError('Primary key is not uuid type')
    except KeyError:
        pass
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


async def prepare(
    endpoint: str,
    *,
    dish: Dish,
    menu_repo: MenuRepository,
    submenu_repo: SubmenuRepository,
    dish_repo: DishRepository
) -> tuple:
    submenu = await submenu_repo.get_or_404(pk=dish.submenu_id)
    menu = await menu_repo.get_or_404(pk=submenu.menu_id)
    res = endpoint.split('/')
    if 'dishes' in res:
        return dish_repo, dish, submenu
    elif 'submenus' in res:
        return submenu_repo, submenu, menu
    return menu_repo, menu, None


def get_endpoint(base_endpoint, parent) -> str:
    if parent is not None:
        base_endpoint = base_endpoint.format(id=parent.id)
    return base_endpoint


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


'''
def check_objs(objs: list[Base], model: Base, size: int = 1) -> None:
    assert isinstance(objs, list)
    assert len(objs) == size
    for obj in objs:
        assert isinstance(obj, model)
'''
