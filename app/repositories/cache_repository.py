from typing import Annotated

from fastapi import Depends

from packages.generic_cache_repo.generic_cache_repository import BaseRedis


class MenuCache(BaseRedis):
    key_prefix = 'menu:'


class SubmenuCache(BaseRedis):
    key_prefix = 'submenu'


class DishCache(BaseRedis):
    key_prefix = 'dish'


menu_cache = Annotated[MenuCache, Depends()]
submenu_cache = Annotated[SubmenuCache, Depends()]
dish_cache = Annotated[DishCache, Depends()]
