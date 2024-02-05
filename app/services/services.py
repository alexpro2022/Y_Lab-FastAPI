from typing import Annotated

from fastapi import Depends

from app.repositories.cache_repository import (dish_cache, menu_cache,
                                               submenu_cache)
from app.repositories.db_repository import dish_crud, menu_crud, submenu_crud
from packages.generic_db_repo.generic_db_repository import ModelType
from packages.generic_service_repo.generic_service_repository import \
    BaseService


class Service(BaseService):

    async def set_cache_on_create(self, obj: ModelType) -> None:
        # return await super().set(obj)
        pass

    async def set_cache_on_update(self, obj: ModelType) -> None:
        pass

    async def set_cache_on_delete(self, obj: ModelType) -> None:
        pass


class MenuService(Service):

    def __init__(self, db: menu_crud, redis: menu_cache):
        super().__init__(db, redis)


class SubmenuService(Service):

    def __init__(self, db: submenu_crud, redis: submenu_cache):
        super().__init__(db, redis)


class DishService(Service):

    def __init__(self, db: dish_crud, redis: dish_cache):
        super().__init__(db, redis)


menu_service = Annotated[MenuService, Depends()]
submenu_service = Annotated[SubmenuService, Depends()]
dish_service = Annotated[DishService, Depends()]
