from httpx import AsyncClient
from app.repositories.db_repository import DishRepository
from app.models.models import Dish, Submenu
from tests.integration_tests.generic_api_tests import GenericAPITests, HTTPMethods

from tests.integration_tests import data as d


class TestMenuAPI(GenericAPITests):
    patch_payload = d.DISH_PATCH_PAYLOAD
    post_payload = d.DISH_POST_PAYLOAD
    expected_results = {
        HTTPMethods.GET: d.CREATED_DISH,
        HTTPMethods.DELETE: d.DELETED_DISH,
        HTTPMethods.PATCH: d.UPDATED_DISH,
        HTTPMethods.POST: d.CREATED_DISH,
    }

    async def test_get_all_returns_empty_list(self, submenu: Submenu, async_client: AsyncClient) -> None:
        self.base_url = d.ENDPOINT_DISH.format(id=submenu.id)
        assert await self.get_test(async_client) == []

    async def test_get_all(self, dish: Dish, dish_repo: DishRepository, async_client: AsyncClient) -> None:
        self.base_url = d.ENDPOINT_DISH.format(id=dish.submenu_id)
        assert await self.get_test(async_client, dish_repo)

    async def test_get(self, dish: Dish, dish_repo: DishRepository, async_client: AsyncClient) -> None:
        self.base_url = d.ENDPOINT_DISH.format(id=dish.submenu_id)
        assert await self.get_test(async_client, dish_repo, dish.id)

    async def test_post(self, submenu: Submenu, dish_repo: DishRepository, async_client: AsyncClient):
        self.base_url = d.ENDPOINT_DISH.format(id=submenu.id)
        assert await self.post_test(async_client, dish_repo)

    async def test_patch(self, dish: Dish, dish_repo: DishRepository, async_client: AsyncClient) -> None:
        self.base_url = d.ENDPOINT_DISH.format(id=dish.submenu_id)
        assert await self.get_test(async_client, dish_repo, dish.id)

    async def test_delete(self, dish: Dish, dish_repo: DishRepository, async_client: AsyncClient) -> None:
        self.base_url = d.ENDPOINT_DISH.format(id=dish.submenu_id)
        assert await self.delete_test(async_client, dish_repo, dish.id)
