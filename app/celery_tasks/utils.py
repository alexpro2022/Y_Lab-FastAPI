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
from packages.generic_db_repo.dependencies import AsyncSessionLocal, get_async_session  # , engine
# import logging

# logging.basicConfig(level=logging.INFO)

FILE_PATH = Path('admin/Menu.xlsx')
TIME_INTERVAL = settings.celery_task_period


def is_modified(fname: Path = FILE_PATH) -> bool:
    mod_time = dt.fromtimestamp(fname.stat().st_mtime)
    return (dt.now() - mod_time).total_seconds() <= TIME_INTERVAL


def get_service(service, session, redis):
    if service is MenuService:
        return MenuService(MenuCRUD(session), MenuCache(redis), None)
    if service is SubmenuService:
        return SubmenuService(SubmenuCRUD(session), SubmenuCache(redis), MenuCache(redis), None)
    if service is DishService:
        return DishService(DishCRUD(session), DishCache(redis), MenuCache(redis), SubmenuCache(redis), None)


async def _dealer(_service, **kwargs):
    redis: aioredis.Redis = get_aioredis()
    async with AsyncSessionLocal() as session:
        service = get_service(_service, session, redis)
        try:
            return await service.db.create(**kwargs)
        except Exception:  # something in DB
            obj = await service.db.get(**kwargs)
            if obj:  # nothing to update
                return obj[0]
            for field in kwargs:
                obj = await service.db.get(**{field: kwargs[field]})
                if obj:
                    break
            if not obj:
                raise ValueError("Couldn't retrieve the object")
            return await service.db.update(**kwargs, id=obj[0].id)


async def clean_repo(_service, ids: set):
    redis: aioredis.Redis = get_aioredis()
    async with AsyncSessionLocal() as session:
        service = get_service(_service, session, redis)
        delete_ids = set([menu.id for menu in await service.db.get()]) - ids
        if delete_ids:
            for id in delete_ids:
                await service.db.delete(id=id)


async def load_data() -> str:
    menu_ids, submenu_ids, dish_ids = set(), set(), set()
    for row in load_workbook(filename=FILE_PATH)['Лист1'].values:
        if row[0] is not None:
            menu = await _dealer(MenuService, title=row[1], description=row[2])
            menu_ids.add(menu.id)
        elif row[1] is not None:
            submenu = await _dealer(SubmenuService, title=row[2], description=row[3], menu_id=menu.id)
            submenu_ids.add(submenu.id)
        else:
            dish = await _dealer(
                DishService, title=row[3], description=row[4], price=str(row[5]), submenu_id=submenu.id)
            dish_ids.add(dish.id)
    await clean_repo(MenuService, menu_ids)
    await clean_repo(SubmenuService, submenu_ids)
    await clean_repo(DishService, dish_ids)
    redis: aioredis.Redis = get_aioredis()
    await redis.flushall()


async def task() -> str | dict[str, str] | None:
    if not is_modified():
        return 'Меню не изменялось. Выход из фоновой задачи...'
    # return await load_data()
