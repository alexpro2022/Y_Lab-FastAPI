from typing import Annotated

from fastapi import Depends
from app.models import Menu, Dish, Submenu
from app.repositories.cache_repository import (dish_cache, menu_cache,
                                               submenu_cache, MENU_PREFIX, SUBMENU_PREFIX, DISH_PREFIX)
from app.repositories.db_repository import dish_crud, menu_crud, submenu_crud
from packages.generic_db_repo.types import ModelType
from packages.generic_service_repo.generic_service_repository import \
    BaseService


class Service(BaseService):

    async def delete(self, **kwargs) -> dict:  # type: ignore [override]
        _ = await super().delete(id=kwargs.get('id'))
        return {'status': True, 'message': f'The {self.db.model.__name__.lower()} has been deleted'}


class MenuService(Service):

    def __init__(self, db: menu_crud, redis: menu_cache, submenu_cache: submenu_cache, dish_cache: dish_cache):
        super().__init__(db, redis)
        self.submenu_cache = submenu_cache
        self.dish_cache = dish_cache

    async def set_cache_on_delete(self, obj: ModelType) -> None:
        await self.cache.delete(obj)
        # delete orphans
        submenus = await self.submenu_cache.get()
        if submenus is None:
            return None
        submenu_names = [self.submenu_cache._get_key(submenu.id) for submenu in submenus if submenu.menu_id == obj.id]
        await self.submenu_cache.delete(submenu_names)
        dishes = await self.dish_cache.get()
        if dishes is None:
            return None
        dish_names = [self.dish_cache._get_key(dish.id) for dish in dishes if dish.submenu_id in submenu_names]
        await self.dish_cache.delete(dish_names)


class SubmenuService(Service):

    def __init__(self, db: submenu_crud, redis: submenu_cache, dish_cache: dish_cache):
        super().__init__(db, redis)
        self.dish_cache = dish_cache

    async def set_cache_on_delete(self, obj: ModelType) -> None:
        await self.cache.delete(obj)
        # delete orphans
        dishes = await self.dish_cache.get()
        if dishes is None:
            return None
        dish_names = [self.dish_cache._get_key(dish.id) for dish in dishes if dish.submenu_id == obj.id]
        await self.dish_cache.delete(dish_names)


class DishService(Service):

    def __init__(self, db: dish_crud, redis: dish_cache):
        super().__init__(db, redis)


menu_service = Annotated[MenuService, Depends()]
submenu_service = Annotated[SubmenuService, Depends()]
dish_service = Annotated[DishService, Depends()]
