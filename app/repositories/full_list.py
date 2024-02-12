from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.models.models import Menu, Submenu
from app.repositories.db_repository import MenuCRUD


async def get_full_list(menu_crud: MenuCRUD):
    menus = await menu_crud.session.scalars(
        select(Menu).options(joinedload(Menu.submenus).joinedload(Submenu.dishes)))
    return menus.unique().all()
