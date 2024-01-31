from typing import Annotated

from fastapi import Depends, HTTPException, status
from sqlalchemy import distinct, func, select
from sqlalchemy.engine import Result

from app.models.models import Dish, Menu, Submenu
from packages.generic_db_repo.dependencies import async_session
from packages.generic_db_repo.generic_db_repository import (CRUDBaseRepository,
                                                            pkType)


class CRUDRepository(CRUDBaseRepository):
    is_delete_allowed_not_in_use = True
    is_update_allowed_not_in_use = True


class MenuRepository(CRUDRepository):
    msg_not_found = 'menu not found'
    msg_already_exists = 'Меню с таким заголовком уже существует.'

    def __init__(self, session: async_session):
        super().__init__(Menu, session)

    async def _get_menu_query(self, **kwargs) -> Result:
        return await self.session.execute(
            select(
                Menu.id,
                Menu.title,
                Menu.description,
                self.model,
                func.count(distinct(Submenu.id)).label('submenus_count'),
                func.count(distinct(Dish.id)).label('dishes_count'),
            )
            .filter_by(**kwargs)
            .outerjoin(Submenu, Menu.id == Submenu.menu_id)
            .outerjoin(Dish, Submenu.id == Dish.submenu_id)
            .group_by(Menu.id)
        )

    async def get_all_(self, exception: bool = False) -> list[Menu]:
        query = await self._get_menu_query()
        all = query.all()
        if not all and exception:
            raise HTTPException(status.HTTP_404_NOT_FOUND, self.msg_not_found)
        return all

    async def get_(self, pk: pkType) -> Menu | None:
        query = await self._get_menu_query(id=pk)
        return query.first()

    async def get_or_404_(self, pk: pkType) -> Menu:
        menu = await self.get_(pk)
        if menu is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, self.msg_not_found)
        return menu


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
