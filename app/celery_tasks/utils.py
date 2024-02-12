from datetime import datetime as dt
from pathlib import Path

from fastapi import HTTPException
from openpyxl import load_workbook
from redis import asyncio as aioredis  # type: ignore [import]
# from sqlalchemy.ext.asyncio import AsyncEngine
# from deepdiff import DeepDiff
from app.core import settings
from app.repositories.cache_repository import (DishCache, MenuCache,
                                               SubmenuCache)
from app.repositories.db_repository import DishCRUD, MenuCRUD, SubmenuCRUD
from app.services.services import DishService, MenuService, SubmenuService
from packages.generic_cache_repo.dependencies import get_aioredis
# from packages.generic_db_repo.base import Base
from packages.generic_db_repo.dependencies import AsyncSessionLocal  # , engine
# import logging

# logging.basicConfig(level=logging.INFO)

FILE_PATH = Path('admin/Menu.xlsx')
TIME_INTERVAL = settings.celery_task_period


def is_modified(fname: Path = FILE_PATH) -> bool:
    mod_time = dt.fromtimestamp(fname.stat().st_mtime)
    return (dt.now() - mod_time).total_seconds() <= TIME_INTERVAL


async def _dealer(service: MenuService | SubmenuService | DishService, **kwargs) -> None:
    service = service.db
    try:
        return await service.create(**kwargs)
    except HTTPException:  # something in DB
        obj = await service.get(**kwargs)
        if obj:  # nothing to update
            return obj[0]
        for field in kwargs:
            obj = await service.get(**{field: kwargs[field]})
            if obj:
                break
        if not obj:
            raise ValueError("Couldn't retrieve the object")
        return await service.update(**kwargs, id=obj[0].id)


def get_rows(fname: str = FILE_PATH):
    return load_workbook(filename=fname)['Лист1'].values


async def fill_repos(menu_service: MenuService,
                     submenu_service: SubmenuService,
                     dish_service: DishService,
                     fname: Path = FILE_PATH) -> None:
    for row in get_rows(fname):
        if row[0] is not None:
            menu = await _dealer(menu_service, title=row[1], description=row[2])
        elif row[1] is not None:
            submenu = await _dealer(submenu_service, title=row[2], description=row[3], menu_id=menu.id)
        else:
            await _dealer(dish_service, title=row[3], description=row[4], price=str(row[5]), submenu_id=submenu.id)


async def load_data() -> str:
    # Rows.rows = get_rows(FILE_PATH)
    redis: aioredis.Redis = get_aioredis()
    # await db_flush()
    await redis.flushall()
    async with AsyncSessionLocal() as session:
        menu_crud = MenuCRUD(session)
        menu_cache = MenuCache(redis)
        submenu_crud = SubmenuCRUD(session)
        submenu_cache = SubmenuCache(redis)
        dish_crud = DishCRUD(session)
        dish_cache = DishCache(redis)
        await fill_repos(MenuService(menu_crud, menu_cache, None),
                         SubmenuService(submenu_crud, submenu_cache, menu_cache, None),
                         DishService(dish_crud, dish_cache, menu_cache, submenu_cache, None))
    return 'Data loading completed'


async def task() -> str | dict[str, str] | None:
    if not is_modified():
        return 'Меню не изменялось. Выход из фоновой задачи...'
    return 'Меню изменялось.'
    # return await load_data()


'''
    menus, _, _ = read_file(FILE_PATH)  # type:ignore [misc]
    if not menus:  # type: ignore [has-type]
        return None
    redis: aioredis.Redis = get_aioredis()
    await redis.flushall()
    await db_flush()
    async with AsyncSessionLocal() as session:
        await fill_repos(menus,
                         MenuService(session, redis, None),
                         SubmenuService(session, redis, None),
                         DishService(session, redis, None))
    return menus



async def submenu_dealer(service: SubmenuService, **kwargs) -> None:
    obj = await service.get(kwargs)
    if obj is None:
        obj = await service.create(**kwargs)
    return obj.id


async def dish_dealer(service: DishService, **kwargs) -> None:
    obj = await service.get(kwargs)
    if obj is None:
        obj = await service.create(**kwargs)
    return obj.id
'''

'''
class Rows:
    rows = None


async def db_flush(engine: AsyncEngine = engine) -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


def periodic_task():
    rows = list(get_rows())
    # print(rows)
    for row
    diff = DeepDiff(Rows.rows, rows)
    return diff

def is_text(value: Any) -> bool:
    try:
        int(value)
    except (TypeError, ValueError):
        return False
    return True

'''
'''async def fill_repos(menus: list[dict],
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
                                   description=dish['description'], price=dish['price']),
                                   extra_data=created_submenu.id) '''
