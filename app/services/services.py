from typing import Annotated

from fastapi import BackgroundTasks, Depends

from app.models import Dish, Menu, Submenu
from app.repositories.cache_repository import dish_cache, menu_cache, submenu_cache
from app.repositories.db_repository import dish_crud, menu_crud, submenu_crud
from packages.generic_service_repo.generic_service_repository import BaseService


class Service(BaseService):

    async def delete(self, **kwargs) -> dict[str, bool | str]:  # type: ignore [override]
        _ = await super().delete(id=kwargs.get('id'))
        return {'message': f'The {self.db.model.__name__.lower()} has been deleted'}


class MenuService(Service):

    def __init__(self, db: menu_crud, redis: menu_cache, bg_tasks: BackgroundTasks) -> None:
        super().__init__(db, redis, bg_tasks)

    async def delete_orphans_cache(self, obj: Menu) -> None:
        # find all the childs by the parent_id
        submenu_keys = await self.cache.get_keys(self.cache.redis, f'*{obj.id}')
        if submenu_keys:
            await self.cache.redis.delete(*submenu_keys)
            for submenu_key in submenu_keys:
                submenu_id = submenu_key.split(':')[1]
                # find all the childs by the parent_id
                dish_keys = await self.cache.get_keys(self.cache.redis, f'*{submenu_id}')
                if dish_keys:
                    await self.cache.redis.delete(*dish_keys)


menu_service = Annotated[MenuService, Depends()]


class SubmenuService(Service):

    def __init__(self, db: submenu_crud, redis: submenu_cache,
                 menu_service: menu_service,
                 bg_tasks: BackgroundTasks) -> None:
        super().__init__(db, redis, bg_tasks)
        self.menu_service = menu_service

    async def refresh_parent_cache(self, submenu: Submenu, *args, **kwargs) -> None:
        menu = await self.menu_service.cache.get(key=submenu.menu_id)
        menu['submenus_count'] += args[0]
        await self.menu_service.cache.set(menu)

    async def delete_orphans_cache(self, obj: Submenu) -> None:
        # find all the childs by the parent_id
        dish_keys = await self.cache.get_keys(self.cache.redis, f'*{obj.id}')
        if dish_keys:
            await self.cache.redis.delete(*dish_keys)


submenu_service = Annotated[SubmenuService, Depends()]


class DishService(Service):

    def __init__(self, db: dish_crud, redis: dish_cache,
                 menu_service: menu_service, submenu_service: submenu_service,
                 bg_tasks: BackgroundTasks) -> None:
        super().__init__(db, redis, bg_tasks)
        self.menu_service = menu_service
        self.submenu_service = submenu_service

    async def refresh_parent_cache(self, dish: Dish, *args, **kwargs) -> None:
        # submenu = await self.submenu_service.refresh(id=dish.submenu_id)  # type: ignore [var-annotated]
        submenu = await self.submenu_service.cache.get(key=dish.submenu_id)
        submenu['dishes_count'] += args[0]
        await self.submenu_service.cache.set(submenu)
        # await self.menu_service.refresh(id=submenu.menu_id)  # type: ignore [attr-defined]
        menu = await self.menu_service.cache.get(key=submenu['menu_id'])
        menu['dishes_count'] += args[0]
        await self.menu_service.cache.set(menu)


dish_service = Annotated[DishService, Depends()]
