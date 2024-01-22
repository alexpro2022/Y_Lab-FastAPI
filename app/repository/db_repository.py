from typing import Annotated, Any
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.models import Dish, Menu, Submenu
from .generic_db_repo.generic_db_repository import CRUDBaseRepository, get_async_session

session = Annotated[AsyncSession, Depends(get_async_session)]


class CRUDRepository(CRUDBaseRepository):
    # the methods are not in use in the project
    def is_update_allowed(self, obj: Any, payload: dict[Any, Any]) -> None:
        pass

    def is_delete_allowed(self, obj: Any) -> None:
        pass


class MenuRepository(CRUDRepository):
    NOT_FOUND = 'menu not found'
    OBJECT_ALREADY_EXISTS = 'Меню с таким заголовком уже существует.'

    def __init__(self, session: session):
        super().__init__(Menu, session)


class SubmenuRepository(CRUDRepository):
    NOT_FOUND = 'submenu not found'
    OBJECT_ALREADY_EXISTS = 'Подменю с таким заголовком уже существует.'

    def __init__(self, session: session):
        super().__init__(Submenu, session)


class DishRepository(CRUDRepository):
    NOT_FOUND = 'dish not found'
    OBJECT_ALREADY_EXISTS = 'Блюдо с таким заголовком уже существует.'

    def __init__(self, session: session):
        super().__init__(Dish, session)


menu_service = Annotated[MenuRepository, Depends()]
submenu_service = Annotated[SubmenuRepository, Depends()]
dish_service = Annotated[DishRepository, Depends()]
