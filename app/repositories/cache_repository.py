from typing import Annotated

from fastapi import Depends

from packages.generic_cache_repo.dependencies import redis
from packages.generic_cache_repo.generic_cache_repository import BaseRedis

MENU_PREFIX = 'menu:'
SUBMENU_PREFIX = 'submenu:'
DISH_PREFIX = 'dish:'


class MenuCache(BaseRedis):

    def __init__(self, redis: redis, redis_expire: int = 3600):
        super().__init__(redis, MENU_PREFIX, redis_expire)


class SubmenuCache(BaseRedis):

    def __init__(self, redis: redis, redis_expire: int = 3600):
        super().__init__(redis, SUBMENU_PREFIX, redis_expire)


class DishCache(BaseRedis):

    def __init__(self, redis: redis, redis_expire: int = 3600):
        super().__init__(redis, DISH_PREFIX, redis_expire)


menu_cache = Annotated[MenuCache, Depends()]
submenu_cache = Annotated[SubmenuCache, Depends()]
dish_cache = Annotated[DishCache, Depends()]
