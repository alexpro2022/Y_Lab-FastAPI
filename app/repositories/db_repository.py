from typing import Annotated

from fastapi import Depends

from app.models.models import Dish, Menu, Submenu
from packages.generic_db_repo.dependencies import async_session
from packages.generic_db_repo.generic_db_repository import CRUDBaseRepository


class CRUDRepository(CRUDBaseRepository):
    is_delete_allowed_not_in_use = True
    is_update_allowed_not_in_use = True


class MenuRepository(CRUDRepository):
    msg_not_found = 'menu not found'
    msg_already_exists = 'Меню с таким заголовком уже существует.'

    def __init__(self, session: async_session):
        super().__init__(Menu, session)


class SubmenuRepository(CRUDRepository):
    msg_not_found = 'submenu not found'
    msg_already_exists = 'Подменю с таким заголовком уже существует.'

    def __init__(self, session: async_session):
        super().__init__(Submenu, session)


class DishRepository(CRUDRepository):
    msg_not_found = 'dish not found'
    msg_already_exists = 'Блюдо с таким заголовком уже существует.'

    def __init__(self, session: async_session):
        super().__init__(Dish, session)


menu_service = Annotated[MenuRepository, Depends()]
submenu_service = Annotated[SubmenuRepository, Depends()]
dish_service = Annotated[DishRepository, Depends()]
