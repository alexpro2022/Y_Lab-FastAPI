from http import HTTPStatus

from deepdiff import DeepDiff
from httpx import AsyncClient

from app.api.endpoints import menu
from app.models.models import Dish, Menu
from app.repositories.db_repository import MenuCRUD
from packages.generic_api.testing_lib import GenericAPITests, HTTPMethods
from tests.fixtures import data as d


class TestMenuAPI(GenericAPITests):
    router = menu.router
    msg_not_found = 'menu not found'
    msg_already_exists = 'Меню с таким заголовком уже существует.'
    patch_payload = d.MENU_PATCH_PAYLOAD
    post_payload = d.MENU_POST_PAYLOAD
    calculated_fields = ('submenus_count', 'dishes_count')
    invalid_id = 1
    expected_results = {
        HTTPMethods.GET: d.CREATED_MENU,
        HTTPMethods.DELETE: d.DELETED_MENU,
        HTTPMethods.PATCH: d.UPDATED_MENU,
        HTTPMethods.POST: d.CREATED_MENU,
    }

    async def test_full_list(self, dish: Dish, async_client: AsyncClient) -> None:
        url = self.reverse('get_full_list_')
        response = await async_client.get(url)
        assert response.status_code == HTTPStatus.OK
        diff = DeepDiff(response.json(),
                        d.FULL_LIST_DATA, exclude_paths=["root[0]['id']",
                                                         "root[0]['submenus'][0]['id']",
                                                         "root[0]['submenus'][0]['dishes'][0]['id']"])
        assert not diff, diff

    async def test_get_all_returns_empty_list(self, init_db, async_client: AsyncClient) -> None:
        url = self.reverse('get_all_menus')
        assert await self.get_test(async_client, url) == []

    async def test_get_all(self, menu: Menu, menu_repo: MenuCRUD, async_client: AsyncClient) -> None:
        url = self.reverse('get_all_menus')
        assert await self.get_test(async_client, url, menu_repo)

    async def test_post(self, init_db, menu_repo: MenuCRUD, async_client: AsyncClient):
        url = self.reverse('create_menu')
        assert await self.post_test(async_client, url, menu_repo)

    async def test_get(self, menu: Menu, menu_repo: MenuCRUD, async_client: AsyncClient) -> None:
        url = self.reverse('get_menu').format(menu_id=menu.id)
        assert await self.get_test(async_client, url, menu_repo)

    async def test_patch(self, menu: Menu, menu_repo: MenuCRUD, async_client: AsyncClient) -> None:
        url = self.reverse('update_menu').format(menu_id=menu.id)
        assert await self.patch_test(async_client, url, menu_repo)

    async def test_delete(self, menu: Menu, menu_repo: MenuCRUD, async_client: AsyncClient) -> None:
        url = self.reverse('delete_menu').format(menu_id=menu.id)
        assert await self.delete_test(async_client, url, menu_repo)
