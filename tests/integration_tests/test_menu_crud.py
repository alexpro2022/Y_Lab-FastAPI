from httpx import AsyncClient
from app.repositories.db_repository import MenuRepository
from app.models.models import Menu
from tests.integration_tests.generic_api_tests import GenericAPITests, HTTPMethods

from tests.integration_tests import data as d


class TestMenuAPI(GenericAPITests):
    base_url = d.ENDPOINT_MENU
    patch_payload = d.MENU_PATCH_PAYLOAD
    post_payload = d.MENU_POST_PAYLOAD
    expected_results = {
        HTTPMethods.GET: d.CREATED_MENU,
        HTTPMethods.DELETE: d.DELETED_MENU,
        HTTPMethods.PATCH: d.UPDATED_MENU,
        HTTPMethods.POST: d.CREATED_MENU,
    }

    async def test_get_all_returns_empty_list(self, init_db, async_client: AsyncClient) -> None:
        assert await self.get_test(async_client) == []

    async def test_get_all(self, menu: Menu, menu_repo: MenuRepository, async_client: AsyncClient) -> None:
        assert await self.get_test(async_client, menu_repo)

    async def test_get(self, menu: Menu, menu_repo: MenuRepository, async_client: AsyncClient) -> None:
        assert await self.get_test(async_client, menu_repo, menu.id)

    async def test_post(self, init_db, menu_repo: MenuRepository, async_client: AsyncClient):
        assert await self.post_test(async_client, menu_repo)

    async def test_patch(self, menu: Menu, menu_repo: MenuRepository, async_client: AsyncClient) -> None:
        assert await self.get_test(async_client, menu_repo, menu.id)

    async def test_delete(self, menu: Menu, menu_repo: MenuRepository, async_client: AsyncClient) -> None:
        assert await self.delete_test(async_client, menu_repo, menu.id)
