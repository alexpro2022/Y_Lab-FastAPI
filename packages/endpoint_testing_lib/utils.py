from http import HTTPStatus

from httpx import AsyncClient, Response

ASSERT_FAIL_MSG = '\nACTUAL:   {}\nEXPECTED: {}'
DONE = 'DONE'


class HTTPMethods:
    GET = 'GET'
    PATCH = 'PATCH'
    POST = 'POST'
    PUT = 'PUT'
    DELETE = 'DELETE'


def dummy_func(*args, **kwargs) -> str:
    return DONE


def get_invalid(item: int | str | dict) -> tuple:
    invalid_str = (None, '', ' ', '-invalid-')
    if isinstance(item, int):
        return 0, -1, 10**12
    if isinstance(item, str):
        return invalid_str
    if isinstance(item, dict):
        dicts = []
        for key in item:
            for invalid_key in invalid_str:
                dd = item.copy()
                value = dd.pop(key)
                dd[invalid_key] = value
                dicts.append(dd)
        return None, *dicts
    raise TypeError('Unsupported type item for get_invalid.')


def strip_slashes(item: int | str | None) -> str:
    return '' if item is None else str(item).lstrip(' /').rstrip(' /').lower()


def create_endpoint(endpoint: str | None, path_param: int | str | None = None) -> str:
    return f'/{strip_slashes(endpoint)}/{strip_slashes(path_param)}'.rstrip(' /')


def assert_msg(response: Response, expected_msg: str | None) -> None:
    if expected_msg is not None:
        actual_msg = response.json()['detail']
        assert actual_msg == expected_msg, ASSERT_FAIL_MSG.format(actual_msg, expected_msg)


def assert_status(response: Response, expected_status_code: int | tuple[int, ...]) -> None:
    if isinstance(expected_status_code, int):
        expected_status_code = (expected_status_code,)
    assert response.status_code in expected_status_code, ASSERT_FAIL_MSG.format(
        response.status_code, expected_status_code)


def get_status_code(method: str):
    match method.upper():
        case HTTPMethods.POST:
            return (HTTPStatus.OK, HTTPStatus.CREATED)
        case HTTPMethods.DELETE:
            return (HTTPStatus.OK, HTTPStatus.NO_CONTENT)
    return HTTPStatus.OK


async def get_response(
    client: AsyncClient,
    method: str,
    endpoint: str,
    *,
    path_param: int | str | None = None,
    params: dict[str, str] | None = None,
    json: dict[str, str] | None = None,
    data: dict | None = None,
    headers: dict | None = None,
) -> Response:
    endpoint = create_endpoint(endpoint, path_param)
    match method.upper():
        case HTTPMethods.GET:
            return await client.get(endpoint, params=params, headers=headers)
        case HTTPMethods.DELETE:
            return await client.delete(endpoint, params=params, headers=headers)
        case HTTPMethods.PATCH:
            return await client.patch(endpoint, params=params, headers=headers, data=data, json=json)
        case HTTPMethods.POST:
            return await client.post(endpoint, params=params, headers=headers, data=data, json=json)
        case HTTPMethods.PUT:
            return await client.put(endpoint, params=params, headers=headers, data=data, json=json)
    raise TypeError('Unsupported HTTP method.')


async def assert_response(
    expected_status_code: int | None,
    client: AsyncClient,
    method: str,
    endpoint: str,
    *,
    path_param: int | str | None = None,
    params: dict[str, str] | None = None,
    data: dict | None = None,
    json: dict[str, str] | None = None,
    headers: dict | None = None,
) -> Response:
    response = await get_response(client, method, endpoint, path_param=path_param,
                                  params=params, data=data, json=json, headers=headers)
    if expected_status_code is None:
        expected_status_code = get_status_code(method)
    assert_status(response, expected_status_code)
    return response
