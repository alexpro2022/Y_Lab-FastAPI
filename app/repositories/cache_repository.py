from typing import Annotated

from fastapi import Depends

from packages.generic_cache_repo.dependencies import redis
from packages.generic_cache_repo.generic_cache_repository import BaseRedis


class MenuCache(BaseRedis):
    key_prefix = 'menu:'

    def __init__(self, redis: redis):
        super().__init__(redis)


class SubmenuCache(BaseRedis):
    key_prefix = 'submenu'

    def __init__(self, redis: redis):
        super().__init__(redis)


class DishCache(BaseRedis):
    key_prefix = 'dish'

    def __init__(self, redis: redis):
        super().__init__(redis)


menu_cache = Annotated[MenuCache, Depends()]
submenu_cache = Annotated[SubmenuCache, Depends()]
dish_cache = Annotated[DishCache, Depends()]
