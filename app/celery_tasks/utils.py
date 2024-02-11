from datetime import datetime as dt
from pathlib import Path

from openpyxl import load_workbook
from redis import asyncio as aioredis  # type: ignore [import]
from sqlalchemy.ext.asyncio import AsyncEngine

from app.core import settings
from app.schemas.schemas import DishIn, MenuIn, SubmenuIn
from app.services.services import DishService, MenuService, SubmenuService
from packages.generic_cache_repo.dependencies import get_aioredis
from packages.generic_db_repo.base import Base
from packages.generic_db_repo.dependencies import engine  # AsyncSessionLocal

FILE_PATH = Path('admin/Menu.xlsx')
TIME_INTERVAL = settings.celery_task_period


def read_file(fname: Path = FILE_PATH) -> tuple[dict[str, str], ...]:
    wb = load_workbook(filename=fname)
    ws = wb['Лист1']
    menus, submenus, dishes = [], [], []
    for row in ws.values:
        if row[0] is not None:
            menu = {}
            menu['title'] = row[1]
            menu['description'] = row[2]
            menu['submenus'] = []
            menus.append(menu)
        elif row[1] is not None:
            submenu = {}
            submenu['title'] = row[2]
            submenu['description'] = row[3]
            submenu['dishes'] = []
            menus[-1]['submenus'].append(submenu)
            submenus.append(submenu)
        else:
            dish = {}
            dish['title'] = row[3]
            dish['description'] = row[4]
            dish['price'] = row[5]
            menus[-1]['submenus'][-1]['dishes'].append(dish)
            dishes.append(dish)
    return menus, submenus, dishes


def is_modified(fname: Path = FILE_PATH) -> bool:
    mod_time = dt.fromtimestamp(fname.stat().st_mtime)
    return (dt.now() - mod_time).total_seconds() <= TIME_INTERVAL


async def db_flush(engine: AsyncEngine = engine) -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def fill_repos(menus: list[dict],
                     menu_service: MenuService,
                     submenu_service: SubmenuService,
                     dish_service: DishService) -> None:
    for menu in menus:
        created_menu = await menu_service.db.create(MenuIn(title=menu['title'], description=menu['description']))
        submenus = menu.get('submenus')
        if submenus:
            for submenu in submenus:
                created_submenu = await submenu_service.db.create(
                    SubmenuIn(title=submenu['title'], description=submenu['description']), extra_data=created_menu.id)
                dishes = submenu.get('dishes')
                if dishes:
                    for dish in dishes:
                        await dish_service.db.create(
                            DishIn(title=dish['title'],
                                   description=dish['description'], price=dish['price']), extra_data=created_submenu.id)


async def task() -> str | dict[str, str] | None:
    if not is_modified():
        return 'Меню не изменялось. Выход из фоновой задачи...'
    menus, _, _ = read_file(FILE_PATH)  # type:ignore [misc]
    if not menus:  # type: ignore [has-type]
        return None
    redis: aioredis.Redis = get_aioredis()
    await redis.flushall()
    await db_flush()
    '''async with AsyncSessionLocal() as session:
        await fill_repos(menus,
                         MenuService(session, redis, None),
                         SubmenuService(session, redis, None),
                         DishService(session, redis, None)) '''
    return menus
