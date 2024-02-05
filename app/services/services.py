from typing import Annotated

from fastapi import Depends
from app.models import Menu, Dish, Submenu
from app.repositories.cache_repository import (dish_cache, menu_cache,
                                               submenu_cache, MENU_PREFIX, SUBMENU_PREFIX, DISH_PREFIX)
from app.repositories.db_repository import dish_crud, menu_crud, submenu_crud
from packages.generic_service_repo.generic_service_repository import \
    BaseService


class MenuService(BaseService):

    def __init__(self, db: menu_crud, redis: menu_cache):
        super().__init__(db, redis)



class SubmenuService(BaseService):

    def __init__(self, db: submenu_crud, redis: submenu_cache):
        super().__init__(db, redis)



class DishService(BaseService):

    def __init__(self, db: dish_crud, redis: dish_cache):
        super().__init__(db, redis)


menu_service = Annotated[MenuService, Depends()]
submenu_service = Annotated[SubmenuService, Depends()]
dish_service = Annotated[DishService, Depends()]
