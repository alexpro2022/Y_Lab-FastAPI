from uuid import uuid4

from httpx import AsyncClient

from app.api.endpoints import dish
from app.models.models import Dish, Submenu
from app.repositories.db_repository import DishCRUD
from packages.generic_api.testing_lib import GenericAPITests, HTTPMethods
from tests.fixtures import data as d

mock_id = uuid4()


class TestDishAPI(GenericAPITests):
    router = dish.router
    msg_not_found = 'dish not found'
    msg_already_exists = 'Блюдо с таким заголовком уже существует.'
    patch_payload = d.DISH_PATCH_PAYLOAD
    post_payload = d.DISH_POST_PAYLOAD
    invalid_id = 1
    expected_results = {
        HTTPMethods.GET: d.CREATED_DISH,
        HTTPMethods.DELETE: d.DELETED_DISH,
        HTTPMethods.PATCH: d.UPDATED_DISH,
        HTTPMethods.POST: d.CREATED_DISH,
    }

    async def test_get_all_returns_empty_list(self, submenu: Submenu, async_client: AsyncClient) -> None:
        url = self.reverse('get_all_dishes').format(menu_id=mock_id, submenu_id=submenu.id)
        assert await self.get_test(async_client, url) == []

    async def test_get_all(self, dish: Dish, dish_repo: DishCRUD, async_client: AsyncClient) -> None:
        url = self.reverse('get_all_dishes').format(menu_id=mock_id, submenu_id=dish.submenu_id)
        assert await self.get_test(async_client, url, dish_repo)

    async def test_post(self, submenu: Submenu, dish_repo: DishCRUD, async_client: AsyncClient):
        url = self.reverse('create_dish').format(menu_id=mock_id, submenu_id=submenu.id)
        assert await self.post_test(async_client, url, dish_repo)

    async def test_get(self, dish: Dish, dish_repo: DishCRUD, async_client: AsyncClient) -> None:
        url = self.reverse('get_dish').format(menu_id=mock_id, submenu_id=dish.submenu_id, dish_id=dish.id)
        assert await self.get_test(async_client, url, dish_repo)

    async def test_patch(self, dish: Dish, dish_repo: DishCRUD, async_client: AsyncClient) -> None:
        url = self.reverse('update_dish').format(menu_id=mock_id, submenu_id=dish.submenu_id, dish_id=dish.id)
        assert await self.patch_test(async_client, url, dish_repo)

    async def test_delete(self, dish: Dish, dish_repo: DishCRUD, async_client: AsyncClient) -> None:
        url = self.reverse('delete_dish').format(menu_id=mock_id, submenu_id=dish.submenu_id, dish_id=dish.id)
        assert await self.delete_test(async_client, url, dish_repo)
