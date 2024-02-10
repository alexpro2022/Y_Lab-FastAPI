from typing import Annotated

from fastapi import Depends

from packages.generic_cache_repo.generic_cache_repository import BaseRedis


class MenuCache(BaseRedis):
    key_prefix = 'menu'


class SubmenuCache(BaseRedis):
    key_prefix = 'submenu'
    parent_id_field_name = 'menu_id'


class DishCache(BaseRedis):
    key_prefix = 'dish'
    parent_id_field_name = 'submenu_id'


menu_cache = Annotated[MenuCache, Depends()]
submenu_cache = Annotated[SubmenuCache, Depends()]
dish_cache = Annotated[DishCache, Depends()]
