from httpx import AsyncClient

from app.models.models import Dish, Submenu
from app.repositories.db_repository import DishCRUD
from packages.generic_api.testing_lib import GenericAPITests, HTTPMethods
from tests.fixtures import data as d


class TestDishAPI(GenericAPITests):
    base_url = d.ENDPOINT_DISH_DEFAULT
    """Needs in parent class for invalid_uuid testing."""
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
        self.base_url = d.ENDPOINT_DISH.format(id=submenu.id)
        assert await self.get_test(async_client) == []

    async def test_get_all(self, dish: Dish, dish_repo: DishCRUD, async_client: AsyncClient) -> None:
        self.base_url = d.ENDPOINT_DISH.format(id=dish.submenu_id)
        assert await self.get_test(async_client, dish_repo)

    async def test_get(self, dish: Dish, dish_repo: DishCRUD, async_client: AsyncClient) -> None:
        self.base_url = d.ENDPOINT_DISH.format(id=dish.submenu_id)
        assert await self.get_test(async_client, dish_repo, dish.id)

    async def test_post(self, submenu: Submenu, dish_repo: DishCRUD, async_client: AsyncClient):
        self.base_url = d.ENDPOINT_DISH.format(id=submenu.id)
        assert await self.post_test(async_client, dish_repo)

    async def test_patch(self, dish: Dish, dish_repo: DishCRUD, async_client: AsyncClient) -> None:
        self.base_url = d.ENDPOINT_DISH.format(id=dish.submenu_id)
        assert await self.patch_test(async_client, dish_repo, dish.id)

    async def test_delete(self, dish: Dish, dish_repo: DishCRUD, async_client: AsyncClient) -> None:
        self.base_url = d.ENDPOINT_DISH.format(id=dish.submenu_id)
        assert await self.delete_test(async_client, dish_repo, dish.id)
