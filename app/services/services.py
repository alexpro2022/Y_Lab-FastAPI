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

    def __init__(self, db: menu_crud, redis: menu_cache,
                 submenu_cache: submenu_cache, dish_cache: dish_cache,
                 bg_tasks: BackgroundTasks) -> None:
        super().__init__(db, redis, bg_tasks)
        self.submenu_cache = submenu_cache
        self.dish_cache = dish_cache

    async def delete_orphans_cache(self, obj: Menu) -> None:
        submenus = await self.submenu_cache.get()
        if submenus is not None:
            submenu_names = [self.submenu_cache._get_key(submenu.id)
                             for submenu in submenus if submenu.menu_id == obj.id]
            await self.submenu_cache.redis.delete(*submenu_names)

        dishes = await self.dish_cache.get()
        if dishes is not None:
            dish_names = [self.dish_cache._get_key(dish.id) for dish in dishes
                          if self.submenu_cache._get_key(dish.submenu_id) in submenu_names]
            await self.dish_cache.redis.delete(*dish_names)


menu_service = Annotated[MenuService, Depends()]


class SubmenuService(Service):

    def __init__(self, db: submenu_crud, redis: submenu_cache,
                 menu_service: menu_service, dish_cache: dish_cache,
                 bg_tasks: BackgroundTasks) -> None:
        super().__init__(db, redis, bg_tasks)
        self.dish_cache = dish_cache
        self.menu_service = menu_service

    async def refresh_parent_cache(self, submenu: Submenu) -> None:
        await self.menu_service.refresh(id=submenu.menu_id)

    async def delete_orphans_cache(self, obj: Submenu) -> None:
        dishes = await self.dish_cache.get()
        if dishes is not None:
            dish_names = [self.dish_cache._get_key(dish.id) for dish in dishes if dish.submenu_id == obj.id]
            await self.dish_cache.redis.delete(*dish_names)


submenu_service = Annotated[SubmenuService, Depends()]


class DishService(Service):

    def __init__(self, db: dish_crud, redis: dish_cache,
                 menu_service: menu_service, submenu_service: submenu_service,
                 bg_tasks: BackgroundTasks) -> None:
        super().__init__(db, redis, bg_tasks)
        self.menu_service = menu_service
        self.submenu_service = submenu_service

    async def refresh_parent_cache(self, dish: Dish) -> None:
        submenu = await self.submenu_service.refresh(id=dish.submenu_id)  # type: ignore [var-annotated]
        await self.menu_service.refresh(id=submenu.menu_id)  # type: ignore [attr-defined]


dish_service = Annotated[DishService, Depends()]
