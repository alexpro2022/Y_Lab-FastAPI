import re

import pytest

from ..utils import *

SLASHLESS = 'SLASHLESS'


def test_dummy_func() -> None:
    assert dummy_func() == DONE


@pytest.mark.parametrize('item, expected_result', (
    (3, (0, -1, 10**12)),
    ('asd', (None, '', ' ', '-invalid-')),
    ({'a': 3}, (None, {None: 3}, {'': 3}, {' ': 3}, {'-invalid-': 3})),
))
def test_get_invalid(item, expected_result) -> None:
    assert get_invalid(item) == expected_result


def test_get_invalid_raises_exception() -> None:
    with pytest.raises(TypeError, match='Unsupported type item for get_invalid.'):
        get_invalid([])  # type: ignore


@pytest.mark.parametrize('item, expected_result', (
    ('', ''), ('  ', ''), ('/', ''), ('///////////', ''),
    (f'/{SLASHLESS}/', SLASHLESS), (f'///{SLASHLESS}///', SLASHLESS),
))
def test_strip_slashes(item: str, expected_result: str) -> None:
    assert strip_slashes(item) == expected_result.lower()


@pytest.mark.parametrize('endpoint', (None, '', ' ', '/', '//', SLASHLESS, f'/{SLASHLESS}/', f'///{SLASHLESS}///'))
@pytest.mark.parametrize('path_param', (None, '', '/', '/1', 1))
def test_create_endpoint(endpoint: str, path_param: str) -> None:
    path = create_endpoint(endpoint, path_param)
    if len(path):
        assert path[0] == '/'
        assert path[-1] != '/'
        assert path.find('none') == -1
    else:
        assert path == ''


class MockResponse:
    def __init__(self, status_code: HTTPStatus = HTTPStatus.OK,
                 json: dict = {'detail': 'mock_response'}):
        self.status_code = status_code
        self._json = json

    # @staticmethod
    def json(self):
        return self._json


class TestAssertMsg:
    response = MockResponse()
    expected_msg = 'mock_response'
    unexpected_msg = 'abc'
    warning_msg = f'\nACTUAL:   {expected_msg}\nEXPECTED: {unexpected_msg}'

    def test_assert_msg_equal(self) -> None:
        assert_msg(self.response, self.expected_msg)

    def test_assert_msg_raises_exception(self) -> None:
        with pytest.raises(AssertionError, match=self.warning_msg):
            assert_msg(self.response, self.unexpected_msg)


class TestAssertStatus:
    response = MockResponse()
    expected_status_code = HTTPStatus.OK
    unexpected_status_code = HTTPStatus.BAD_GATEWAY
    warning_msg = f'\nACTUAL:   {expected_status_code}\nEXPECTED: {(unexpected_status_code,)}'

    def test_assert_status_equal(self) -> None:
        assert_status(self.response, self.expected_status_code)

    def test_assert_status_raises_exception(self) -> None:
        with pytest.raises(AssertionError, match=re.escape(self.warning_msg)):
            assert_status(self.response, self.unexpected_status_code)


@pytest.mark.parametrize('method, expected_result', (
    (HTTPMethods.POST, (HTTPStatus.OK, HTTPStatus.CREATED)),
    (HTTPMethods.DELETE, (HTTPStatus.OK, HTTPStatus.NO_CONTENT)),
    (HTTPMethods.GET, HTTPStatus.OK),
    (HTTPMethods.PATCH, HTTPStatus.OK),
    (HTTPMethods.PUT, HTTPStatus.OK),
))
def test_get_status_code(method, expected_result) -> None:
    assert get_status_code(method) == expected_result


async def test_get_response_raises_exception() -> None:
    with pytest.raises(TypeError, match='Unsupported HTTP method.'):
        await get_response(AsyncClient(), '', '')


parametrize = pytest.mark.parametrize('method, func_to_mock', (
    (HTTPMethods.GET, 'httpx.AsyncClient.get'),
    (HTTPMethods.DELETE, 'httpx.AsyncClient.delete'),
    (HTTPMethods.PATCH, 'httpx.AsyncClient.patch'),
    (HTTPMethods.POST, 'httpx.AsyncClient.post'),
    (HTTPMethods.PUT, 'httpx.AsyncClient.put'),
))


async def generic_test_for_get_response_and_assert_response(monkeypatch, method, func_to_mock, coro) -> None:
    async def mock(*args, **kwargs) -> MockResponse:
        return MockResponse(json={'detail': method})

    monkeypatch.setattr(func_to_mock, mock)
    response = await coro
    assert response.json()['detail'] == method


@parametrize
async def test_get_response(monkeypatch, method, func_to_mock) -> None:
    coro = get_response(AsyncClient(), method, '')
    await generic_test_for_get_response_and_assert_response(monkeypatch, method, func_to_mock, coro)


@parametrize
async def test_assert_response(monkeypatch, method, func_to_mock) -> None:
    coro = assert_response(None, AsyncClient(), method, '')
    await generic_test_for_get_response_and_assert_response(monkeypatch, method, func_to_mock, coro)


@parametrize
async def test_assert_response_raises_exception(monkeypatch, method, func_to_mock) -> None:
    coro = assert_response(HTTPStatus.BAD_GATEWAY, AsyncClient(), method, '')
    with pytest.raises(AssertionError):
        await generic_test_for_get_response_and_assert_response(monkeypatch, method, func_to_mock, coro)
