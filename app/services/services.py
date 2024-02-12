from typing import Annotated

from fastapi import BackgroundTasks, Depends

from app.models import Dish, Menu, Submenu
from app.repositories.cache_repository import (dish_cache, menu_cache,
                                               submenu_cache)
from app.repositories.db_repository import dish_crud, menu_crud, submenu_crud
from packages.generic_service_repo.generic_service_repository import \
    BaseService


class Service(BaseService):

    async def delete(self, **kwargs) -> dict[str, bool | str]:  # type: ignore [override]
        _ = await super().delete(id=kwargs.get('id'))
        return {'message': f'The {self.db.model.__name__.lower()} has been deleted'}


class MenuService(Service):

    def __init__(self, db: menu_crud, redis: menu_cache, bg_tasks: BackgroundTasks) -> None:
        super().__init__(db, redis, bg_tasks)

    async def set_cache_on_delete(self, obj: Menu) -> None:
        await super().set_cache_on_delete(obj)
        # Delete orphans
        # find childs by the parent_id
        submenu_keys = await self.cache.get_keys(self.cache.redis, f'*{obj.id}')
        if submenu_keys:
            await self.cache.delete(*submenu_keys)
            for submenu_key in submenu_keys:
                submenu_id = submenu_key.split(':')[1]
                # find childs by the parent_id
                dish_keys = await self.cache.get_keys(self.cache.redis, f'*{submenu_id}')
                await self.cache.delete(*dish_keys)


class SubmenuService(Service):

    def __init__(self, db: submenu_crud, redis: submenu_cache,
                 menu_cache: menu_cache, bg_tasks: BackgroundTasks) -> None:
        super().__init__(db, redis, bg_tasks)
        self.menu_cache = menu_cache

    async def set_cache_on_create(self, obj: Submenu) -> None:
        menu = await self.menu_cache.get(key=obj.menu_id)
        # self.menu_cache.redis.hincrby('submenus_count', 1)
        if menu:
            menu['submenus_count'] += 1
            await self.menu_cache.set(menu)

    async def set_cache_on_delete(self, obj: Submenu) -> None:
        await super().set_cache_on_delete(obj)
        # Delete orphans
        dish_keys = await self.cache.get_keys(self.cache.redis, f'*{obj.id}')
        await self.cache.delete(*dish_keys)
        # Refresh parent cache
        menu = await self.menu_cache.get(key=obj.menu_id)
        if menu:
            menu['submenus_count'] -= 1
            menu['dishes_count'] -= len(dish_keys)
            await self.menu_cache.set(menu)


class DishService(Service):

    def __init__(self, db: dish_crud, redis: dish_cache,
                 menu_cache: menu_cache, submenu_cache: submenu_cache,
                 bg_tasks: BackgroundTasks) -> None:
        super().__init__(db, redis, bg_tasks)
        self.menu_cache = menu_cache
        self.submenu_cache = submenu_cache

    async def refresh_parent_cache(self, dish: Dish, counter: int) -> None:
        submenu = await self.submenu_cache.get(key=dish.submenu_id)
        if submenu:
            submenu['dishes_count'] += counter
            await self.submenu_cache.set(submenu)
            menu = await self.menu_cache.get(key=submenu['menu_id'])
            if menu:
                menu['dishes_count'] += counter
                await self.menu_cache.set(menu)

    async def set_cache_on_create(self, obj: Dish) -> None:
        await self.refresh_parent_cache(obj, counter=1)

    async def set_cache_on_delete(self, obj: Dish) -> None:
        await super().set_cache_on_delete(obj)
        await self.refresh_parent_cache(obj, counter=-1)


menu_service = Annotated[MenuService, Depends()]
submenu_service = Annotated[SubmenuService, Depends()]
dish_service = Annotated[DishService, Depends()]
