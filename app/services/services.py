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
        submenu_names = [key.decode('utf-8') for key in await self.cache.redis.keys(f'*{obj.id}')]
        print(submenu_names)
        if submenu_names:
            await self.cache.redis.delete(*submenu_names)
            for submenu_name in submenu_names:
                print(submenu_name)
                submenu_name = submenu_name.split(':')[1]
                print(submenu_name)
                dish_names = [key.decode('utf-8') for key in await self.cache.redis.keys(f'*{submenu_name}')]
                print(dish_names)
                if dish_names:
                    await self.cache.redis.delete(*dish_names)


menu_service = Annotated[MenuService, Depends()]


class SubmenuService(Service):

    def __init__(self, db: submenu_crud, redis: submenu_cache,
                 menu_service: menu_service,
                 bg_tasks: BackgroundTasks) -> None:
        super().__init__(db, redis, bg_tasks)
        self.menu_service = menu_service

    async def refresh_parent_cache(self, submenu: Submenu) -> None:
        await self.menu_service.refresh(id=submenu.menu_id)

    async def delete_orphans_cache(self, obj: Submenu) -> None:
        dish_names = [key.decode('utf-8') for key in await self.cache.redis.keys(f'*{obj.id}')]
        print(dish_names)
        if dish_names:
            await self.cache.redis.delete(*dish_names)


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
