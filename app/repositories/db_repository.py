from typing import Annotated

from fastapi import Depends
from sqlalchemy import Select, distinct, func, select

from app.models.models import Dish, Menu, Submenu
from packages.generic_db_repo.dependencies import async_session
from packages.generic_db_repo.generic_db_repository import BaseCRUD


class CRUD(BaseCRUD):
    has_permission_not_in_use = True
    is_delete_allowed_not_in_use = True
    is_update_allowed_not_in_use = True


class MenuCRUD(CRUD):
    msg_not_found = 'menu not found'
    msg_already_exists = 'Меню с таким заголовком уже существует.'

    def __init__(self, session: async_session):
        super().__init__(Menu, session)

    def get_statement(self, **kwargs) -> Select:
        return (
            select(
                Menu.id,
                Menu.title,
                Menu.description,
                func.count(distinct(Submenu.id)).label('submenus_count'),
                func.count(distinct(Dish.id)).label('dishes_count'),
            )
            .filter_by(**kwargs)
            .outerjoin(Submenu, Menu.id == Submenu.menu_id)
            .outerjoin(Dish, Submenu.id == Dish.submenu_id)
            .group_by(Menu.id)
        )


class SubmenuCRUD(CRUD):
    msg_not_found = 'submenu not found'
    msg_already_exists = 'Подменю с таким заголовком уже существует.'

    def __init__(self, session: async_session):
        super().__init__(Submenu, session)

    def get_statement(self, **kwargs) -> Select:
        return (
            select(
                Submenu.id,
                Submenu.title,
                Submenu.description,
                Submenu.menu_id,
                func.count(distinct(Dish.id)).label('dishes_count'),
            )
            .filter_by(**kwargs)
            .outerjoin(Dish, Submenu.id == Dish.submenu_id)
            .group_by(Submenu.id)
        )


class DishCRUD(CRUD):
    msg_not_found = 'dish not found'
    msg_already_exists = 'Блюдо с таким заголовком уже существует.'

    def __init__(self, session: async_session):
        super().__init__(Dish, session)


menu_service = Annotated[MenuCRUD, Depends()]
submenu_service = Annotated[SubmenuCRUD, Depends()]
dish_service = Annotated[DishCRUD, Depends()]
