import typing

from deepdiff import DeepDiff

from packages.endpoint_testing_lib.utils import DONE
from tests import conftest as c
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


def check_full_list(response_json: dict) -> str:
    return _check_response(response_json, d.EXPECTED_FULL_LIST)


def get_crud(endpoint, *,
             menu_repo: c.MenuRepository,
             submenu_repo: c.SubmenuRepository,
             dish_repo: c.DishRepository
             ) -> c.MenuRepository | c.SubmenuRepository | c.DishRepository:
    res = endpoint.split('/')
    if 'dishes' in res:
        return dish_repo
    elif 'submenus' in res:
        return submenu_repo
    return menu_repo


def compare(left: c.Base, right: c.Base) -> None:
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


def compare_lists(left: list[c.Base], right: list[c.Base]) -> None:
    assert left
    assert right
    size_left = len(left)
    assert size_left == len(right)
    for i in range(size_left):
        compare(left[i], right[i])


'''
def check_exception_info(exc_info, expected_msg: str, expected_error_code: int | None = None) -> None:
    if expected_error_code is None:
        assert exc_info.value.args[0] == expected_msg
    else:
        for index, item in enumerate((expected_error_code, expected_msg)):
            assert exc_info.value.args[index] == item, (exc_info.value.args[index], item)


def check_exception_info_not_found(exc_info, msg_not_found: str) -> None:
    check_exception_info(exc_info, msg_not_found, status.HTTP_404_NOT_FOUND)



class CRUD():

    def is_update_allowed(self, obj: c.Model | None, payload: dict | None) -> None:
        pass

    def is_delete_allowed(self, obj: c.Model | None) -> None:
        pass

    def perform_create(self, create_data: dict, extra_data: typing.Any | None = None) -> None:
        create_data['title'] = extra_data

    def perform_update(self, obj: typing.Any, update_data: dict) -> typing.Any | None:
        update_data['title'] = 'perform_updated_done'
        for key, value in update_data.items():
            setattr(obj, key, value)
        return obj
'''
