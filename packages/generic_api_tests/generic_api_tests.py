from http import HTTPStatus
from typing import Any, TypeAlias
from uuid import UUID

from httpx import AsyncClient
from sqlalchemy import Row
from packages.generic_db_repo.generic_db_repository import BaseCRUD

Json: TypeAlias = dict[str, str]
DONE = 'DONE'


class HTTPMethods:
    GET = 'GET'
    PATCH = 'PATCH'
    POST = 'POST'
    PUT = 'PUT'
    DELETE = 'DELETE'


class GenericAPITests:
    base_url: str
    msg_not_found: str
    msg_already_exists: str
    post_payload: Json
    patch_payload: Json
    expected_results: dict[str, Json | dict[str, Any] | None] = {
        HTTPMethods.GET: None,
        HTTPMethods.PATCH: None,
        HTTPMethods.POST: None,
        HTTPMethods.DELETE: None,
    }

    def get_endpoint(self, idx: UUID | None = None) -> str:
        return self.base_url if idx is None else f'{self.base_url}/{idx}'

    async def _compare_with_db(self, response_json: Json, pk: UUID, repo: BaseCRUD) -> None:
        obj = await repo.get(id=pk, exception=True)
        if not isinstance(obj, Row):
            await repo.session.refresh(obj)
        for key in response_json:
            if key not in ('submenus_count', 'dishes_count'):
                assert getattr(obj, key, None) == response_json[key]

    async def check_response(self, response_json: dict | list[dict], expected_result: dict | list[dict], repo) -> str:
        assert type(response_json) is type(expected_result)
        if isinstance(response_json, list):
            response_json = response_json[0]
            expected_result = expected_result[0]
        assert isinstance(response_json, dict)
        assert isinstance(expected_result, dict)
        try:
            pk = UUID(str(response_json.pop('id')))
        except ValueError:
            raise AssertionError('Primary key is not uuid type')
        except KeyError:
            pk = None
        if pk is not None:
            await self._compare_with_db(response_json, pk, repo)
        assert response_json.items() == expected_result.items()
        return DONE

    async def get_test(self, async_client: AsyncClient, repo: BaseCRUD | None = None,
                       idx: UUID | None = None) -> Json | list[Json]:
        response = await async_client.get(self.get_endpoint(idx))
        assert response.status_code == HTTPStatus.OK
        response_json = response.json()
        if response_json:
            expected_result = ([self.expected_results[HTTPMethods.GET]] if isinstance(response_json, list) else
                               self.expected_results[HTTPMethods.GET])
            assert await self.check_response(response_json, expected_result, repo) == DONE  # type: ignore [arg-type]
        return response.json()

    async def patch_test(self, async_client: AsyncClient, repo: BaseCRUD, idx: UUID) -> Json:
        response = await async_client.patch(self.get_endpoint(idx), json=self.patch_payload)
        assert response.status_code == HTTPStatus.OK, response.json()
        assert await self.check_response(
            response.json(), self.expected_results[HTTPMethods.PATCH], repo) == DONE  # type: ignore [arg-type]
        return response.json()

    async def post_test(self, async_client: AsyncClient, repo: BaseCRUD) -> Json:
        response = await async_client.post(self.base_url, json=self.post_payload)
        assert response.status_code == HTTPStatus.CREATED
        r = await async_client.post(self.base_url, json=self.post_payload)
        assert r.status_code == HTTPStatus.BAD_REQUEST
        assert r.json().get('detail') == self.msg_already_exists
        assert await self.check_response(
            response.json(), self.expected_results[HTTPMethods.POST], repo) == DONE  # type: ignore [arg-type]
        return response.json()

    async def delete_test(self, async_client: AsyncClient, repo: BaseCRUD, idx: UUID) -> Json:
        response = await async_client.delete(self.get_endpoint(idx))
        assert response.status_code == HTTPStatus.OK
        r = await async_client.delete(self.get_endpoint(idx))
        assert r.status_code == HTTPStatus.NOT_FOUND
        assert r.json().get('detail') == self.msg_not_found
        assert await self.check_response(
            response.json(), self.expected_results[HTTPMethods.DELETE], repo) == DONE  # type: ignore [arg-type]
        return response.json()
