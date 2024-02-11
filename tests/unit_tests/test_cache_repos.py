from uuid import uuid4

from app.models import Dish, Menu, Submenu
from app.repositories.cache_repository import DishCache, MenuCache, SubmenuCache
from packages.generic_cache_repo.testing_tools.testing_lib import BaseRedisTest
from tests.fixtures import data as d

ID = {'id': uuid4()}


class TestMenuCache(BaseRedisTest):
    cache = MenuCache
    model = Menu
    create_data = {**ID, **d.MENU_POST_PAYLOAD}


class TestSubmenuCache(BaseRedisTest):
    cache = SubmenuCache
    model = Submenu
    create_data = {**ID, **d.SUBMENU_POST_PAYLOAD, 'menu_id': uuid4()}


class TestDishCache(BaseRedisTest):
    cache = DishCache
    model = Dish
    create_data = {**ID, **d.DISH_POST_PAYLOAD, 'submenu_id': uuid4()}
