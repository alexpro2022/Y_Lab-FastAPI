from typing import Annotated

from fastapi import Depends
# from app.models import Menu, Dish, Submenu
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
        if submenus is not None:
            submenu_names = [self.submenu_cache._get_key(submenu.id) for submenu in submenus if submenu.menu_id == obj.id]
            await self.submenu_cache.redis.delete(*submenu_names)

        dishes = await self.dish_cache.get()
        if dishes is not None:
            dish_names = [self.dish_cache._get_key(dish.id) for dish in dishes if dish.submenu_id in submenu_names]
            await self.dish_cache.redis.delete(*dish_names)


menu_service = Annotated[MenuService, Depends()]


class SubmenuService(Service):

    def __init__(self, db: submenu_crud, redis: submenu_cache, menu_service: menu_service, dish_cache: dish_cache):
        super().__init__(db, redis)
        self.dish_cache = dish_cache
        self.menu_service = menu_service

    '''async def get(self, exception: bool = False, **kwargs) -> ModelType | list[ModelType] | None:
        assert await self.cache.get() is None
        entity_from_db = await super().get(exception, **kwargs)
        entity_from_cache = await self.cache.get()[0]  # await super().get(exception, **kwargs)
        print(entity_from_db)
        print(entity_from_cache[0])
        assert 0
        dishes = await self.dish_cache.get()
        if dishes is not None:
            if isinstance(entity, (list, tuple)):
                for item in entity:
                    item.dishes_count = len([dish for dish in dishes if dish.submenu_id == item.id])
            else:
                entity.dishes_count = len([dish for dish in dishes if dish.submenu_id == entity.id])
            print(entity)
            return entity '''

    async def set_cache_on_create(self, obj: ModelType) -> None:
        await super().set_cache_on_create(obj)
        # Refreshing parent cache
        await self.menu_service.refresh(id=obj.menu_id)

    async def set_cache_on_delete(self, obj: ModelType) -> None:
        await self.cache.delete(obj)
        # delete orphans
        dishes = await self.dish_cache.get()
        if dishes is not None:
            dish_names = [self.dish_cache._get_key(dish.id) for dish in dishes if dish.submenu_id == obj.id]
            await self.dish_cache.redis.delete(*dish_names)
        # Refreshing parent cache
        await self.menu_service.refresh(id=obj.menu_id)


submenu_service = Annotated[SubmenuService, Depends()]


class DishService(Service):

    def __init__(self, db: dish_crud, redis: dish_cache, menu_service: menu_service, submenu_service: submenu_service):
        super().__init__(db, redis)
        self.menu_service = menu_service
        self.submenu_service = submenu_service

    async def set_cache_on_create(self, obj: ModelType) -> None:
        await super().set_cache_on_create(obj)
        # Refreshing parent cache
        submenu = await self.submenu_service.refresh(id=obj.submenu_id)
        await self.menu_service.refresh(submenu.menu_id)

    async def set_cache_on_delete(self, obj: ModelType) -> None:
        await self.cache.delete(obj)
        # Refreshing parent cache
        submenu = await self.submenu_service.refresh(id=obj.submenu_id)
        await self.menu_service.refresh(submenu.menu_id)


dish_service = Annotated[DishService, Depends()]
