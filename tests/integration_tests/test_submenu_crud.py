from httpx import AsyncClient

from app.models.models import Menu, Submenu
from app.repositories.db_repository import SubmenuCRUD
from packages.generic_api_tests.generic_api_tests import (GenericAPITests,
                                                          HTTPMethods)
from tests.fixtures import data as d


class TestSubmenuAPI(GenericAPITests):
    base_url = d.ENDPOINT_SUBMENU_DEFAULT
    """Needs in parent class for invalid_uuid testing."""
    msg_not_found = 'submenu not found'
    msg_already_exists = 'Подменю с таким заголовком уже существует.'
    patch_payload = d.SUBMENU_PATCH_PAYLOAD
    post_payload = d.SUBMENU_POST_PAYLOAD
    calculated_fields = ('dishes_count',)
    invalid_id = 1
    expected_results = {
        HTTPMethods.GET: d.CREATED_SUBMENU,
        HTTPMethods.DELETE: d.DELETED_SUBMENU,
        HTTPMethods.PATCH: d.UPDATED_SUBMENU,
        HTTPMethods.POST: d.CREATED_SUBMENU,
    }

    async def test_get_all_returns_empty_list(self, menu: Menu, async_client: AsyncClient) -> None:
        self.base_url = d.ENDPOINT_SUBMENU.format(id=menu.id)
        assert await self.get_test(async_client) == []

    async def test_get_all(self, submenu: Submenu, submenu_repo: SubmenuCRUD, async_client: AsyncClient) -> None:
        self.base_url = d.ENDPOINT_SUBMENU.format(id=submenu.menu_id)
        assert await self.get_test(async_client, submenu_repo)

    async def test_get(self, submenu: Submenu, submenu_repo: SubmenuCRUD, async_client: AsyncClient) -> None:
        self.base_url = d.ENDPOINT_SUBMENU.format(id=submenu.menu_id)
        assert await self.get_test(async_client, submenu_repo, submenu.id)

    async def test_post(self, menu: Menu, submenu_repo: SubmenuCRUD, async_client: AsyncClient):
        self.base_url = d.ENDPOINT_SUBMENU.format(id=menu.id)
        assert await self.post_test(async_client, submenu_repo)

    async def test_patch(self, submenu: Submenu, submenu_repo: SubmenuCRUD, async_client: AsyncClient) -> None:
        self.base_url = d.ENDPOINT_SUBMENU.format(id=submenu.menu_id)
        assert await self.patch_test(async_client, submenu_repo, submenu.id)

    async def test_delete(self, submenu: Submenu, submenu_repo: SubmenuCRUD, async_client: AsyncClient) -> None:
        self.base_url = d.ENDPOINT_SUBMENU.format(id=submenu.menu_id)
        assert await self.delete_test(async_client, submenu_repo, submenu.id)
