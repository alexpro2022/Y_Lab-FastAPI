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

    # Valid_request_test -----------------------------------------------------------------------------------
    response = await assert_response(
        None, client, method, endpoint, path_param=path_param, params=params, json=json, data=data, headers=headers)
    # if func_check_valid_response is None:
    #    func_check_valid_response = dummy_func
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

'''
    # invalid_endpoint_test -----------------------------------------------------------------------------------
    for invalid_endpoint in get_invalid(endpoint):
        await assert_response(
            HTTPStatus.NOT_FOUND, client, method, invalid_endpoint, path_param=path_param,
            params=params, json=json, data=data, headers=headers)  # type: ignore [arg-type]

    # invalid_path_param_test -----------------------------------------------------------------------------------
    if path_param is not None:
        for invalid_path_param in get_invalid(path_param):
            r = await assert_response(
                HTTPStatus.NOT_FOUND, client, method, endpoint, path_param=invalid_path_param,
                params=params, json=json, data=data, headers=headers)  # type: ignore [arg-type]
            assert_msg(r, msg_not_found)

    # invalid_query_params_keys_test -----------------------------------------------------------------------------------
    if params is not None and check_params:
        for invalid_params_keys in get_invalid(params):
            await assert_response(
                HTTPStatus.UNPROCESSABLE_ENTITY, client, method, endpoint, path_param=path_param,
                params=invalid_params_keys, json=json, data=data, headers=headers)  # type: ignore [arg-type]

    # invalid_payload_keys_test -----------------------------------------------------------------------------------
    if json is not None and check_json:
        for invalid_json_keys in get_invalid(json):
            await assert_response(
                HTTPStatus.UNPROCESSABLE_ENTITY, client, method, endpoint, path_param=path_param,
                params=params, json=invalid_json_keys, data=data, headers=headers)  # type: ignore [arg-type]

    # invalid_form_keys_test -----------------------------------------------------------------------------------
    if data is not None and check_data:
        for invalid_data_keys in get_invalid(data):
            await assert_response(
                HTTPStatus.UNPROCESSABLE_ENTITY, client, method, endpoint, path_param=path_param,
                params=params, json=json, data=invalid_data_keys, headers=headers)  # type: ignore [arg-type]
'''
