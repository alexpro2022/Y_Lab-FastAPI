from httpx import AsyncClient

from app.api.endpoints import submenu
from app.models.models import Menu, Submenu
from app.repositories.db_repository import SubmenuCRUD
from packages.generic_api.testing_lib import GenericAPITests, HTTPMethods
from tests.fixtures import data as d


class TestSubmenuAPI(GenericAPITests):
    router = submenu.router
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
        url = self.reverse('get_all_submenus').format(menu_id=menu.id)
        assert await self.get_test(async_client, url) == []

    async def test_get_all(self, submenu: Submenu, submenu_repo: SubmenuCRUD, async_client: AsyncClient) -> None:
        url = self.reverse('get_all_submenus').format(menu_id=submenu.menu_id)
        assert await self.get_test(async_client, url, submenu_repo)

    async def test_post(self, menu: Menu, submenu_repo: SubmenuCRUD, async_client: AsyncClient):
        url = self.reverse('get_all_submenus').format(menu_id=menu.id)
        assert await self.post_test(async_client, url, submenu_repo)

    async def test_get(self, submenu: Submenu, submenu_repo: SubmenuCRUD, async_client: AsyncClient) -> None:
        url = self.reverse('get_submenu').format(menu_id=submenu.menu_id, submenu_id=submenu.id)
        assert await self.get_test(async_client, url, submenu_repo)

    async def test_patch(self, submenu: Submenu, submenu_repo: SubmenuCRUD, async_client: AsyncClient) -> None:
        url = self.reverse('get_submenu').format(menu_id=submenu.menu_id, submenu_id=submenu.id)
        assert await self.patch_test(async_client, url, submenu_repo)

    async def test_delete(self, submenu: Submenu, submenu_repo: SubmenuCRUD, async_client: AsyncClient) -> None:
        url = self.reverse('get_submenu').format(menu_id=submenu.menu_id, submenu_id=submenu.id)
        assert await self.delete_test(async_client, url, submenu_repo)
