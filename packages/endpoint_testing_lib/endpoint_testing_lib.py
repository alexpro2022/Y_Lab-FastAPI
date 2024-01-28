from typing import Callable

from .utils import *


async def not_allowed_methods_test(
    client: AsyncClient,
    not_allowed_methods: tuple[str, ...],
    endpoint: str,
    path_param: int | str | None = None,
) -> None:
    for method in not_allowed_methods:
        await assert_response(HTTPStatus.METHOD_NOT_ALLOWED, client, method, endpoint, path_param=path_param)


async def standard_tests(
    client: AsyncClient,
    method: str,
    endpoint: str,
    *,
    path_param: int | str | None = None,
    params: dict[str, str] | None = None,
    check_params: bool = False,
    json: dict[str, str] | None = None,
    check_json: bool = False,
    data: dict[str, str] | None = None,
    check_data: bool = False,
    headers: dict | None = None,
    func_check_valid_response: Callable = dummy_func,
    msg_already_exists: str | None = None,
    msg_not_found: str | None = None,
) -> None:
    method = method.upper()
    response = await assert_response(
        None, client, method, endpoint, path_param=path_param, params=params, json=json, data=data, headers=headers)
    assert func_check_valid_response(response.json()) == DONE
    # Extra tests for valid request:
    # testing uniqueness:
    if method == HTTPMethods.POST and msg_already_exists is not None:
        # Sequential POST with the same data should get Integrity Error which raises BAD_REQUEST
        r = await assert_response(
            HTTPStatus.BAD_REQUEST, client, method, endpoint, path_param=path_param,
            params=params, json=json, data=data, headers=headers)
        assert_msg(r, msg_already_exists)
    elif method == HTTPMethods.DELETE:
        # Sequential DELETE with the same data should get NOT_FOUND
        r = await assert_response(
            HTTPStatus.NOT_FOUND, client, method, endpoint, path_param=path_param,
            params=params, json=json, data=data, headers=headers)
        assert_msg(r, msg_not_found)
