from httpx import AsyncClient
from app.repositories.db_repository import SubmenuRepository
from app.models.models import Menu, Submenu
from tests.integration_tests.generic_api_tests import GenericAPITests, HTTPMethods

from tests.integration_tests import data as d


class TestMenuAPI(GenericAPITests):
    patch_payload = d.SUBMENU_PATCH_PAYLOAD
    post_payload = d.SUBMENU_POST_PAYLOAD
    expected_results = {
        HTTPMethods.GET: d.CREATED_SUBMENU,
        HTTPMethods.DELETE: d.DELETED_SUBMENU,
        HTTPMethods.PATCH: d.UPDATED_SUBMENU,
        HTTPMethods.POST: d.CREATED_SUBMENU,
    }

    async def test_get_all_returns_empty_list(self, menu: Menu, async_client: AsyncClient) -> None:
        self.base_url = d.ENDPOINT_SUBMENU.format(id=menu.id)
        assert await self.get_test(async_client) == []

    async def test_get_all(self, submenu: Submenu, submenu_repo: SubmenuRepository, async_client: AsyncClient) -> None:
        self.base_url = d.ENDPOINT_SUBMENU.format(id=submenu.menu_id)
        assert await self.get_test(async_client, submenu_repo)

    async def test_get(self, submenu: Submenu, submenu_repo: SubmenuRepository, async_client: AsyncClient) -> None:
        self.base_url = d.ENDPOINT_SUBMENU.format(id=submenu.menu_id)
        assert await self.get_test(async_client, submenu_repo, submenu.id)

    async def test_post(self, menu: Menu, submenu_repo: SubmenuRepository, async_client: AsyncClient):
        self.base_url = d.ENDPOINT_SUBMENU.format(id=menu.id)
        assert await self.post_test(async_client, submenu_repo)

    async def test_patch(self, submenu: Submenu, submenu_repo: SubmenuRepository, async_client: AsyncClient) -> None:
        self.base_url = d.ENDPOINT_SUBMENU.format(id=submenu.menu_id)
        assert await self.get_test(async_client, submenu_repo, submenu.id)

    async def test_delete(self, submenu: Submenu, submenu_repo: SubmenuRepository, async_client: AsyncClient) -> None:
        self.base_url = d.ENDPOINT_SUBMENU.format(id=submenu.menu_id)
        assert await self.delete_test(async_client, submenu_repo, submenu.id)
