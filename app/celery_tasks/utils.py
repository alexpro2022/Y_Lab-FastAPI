from datetime import datetime as dt
from pathlib import Path

from openpyxl import load_workbook
from redis import asyncio as aioredis  # type: ignore [import]

from app.core import settings
from app.repositories.db_repository import DishCRUD, MenuCRUD, SubmenuCRUD
from packages.generic_cache_repo.dependencies import get_aioredis
from packages.generic_db_repo.dependencies import AsyncSessionLocal

FILE_PATH = Path('admin/Menu.xlsx')
TIME_INTERVAL = settings.celery_task_period


def is_modified(fname: Path = FILE_PATH) -> bool:
    mod_time = dt.fromtimestamp(fname.stat().st_mtime)
    return (dt.now() - mod_time).total_seconds() <= TIME_INTERVAL


async def _dealer(crud, **kwargs):
    async with AsyncSessionLocal() as session:
        service = crud(session)
        try:
            return await service.create(**kwargs)
        except Exception:  # something in DB
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


async def clean_repo(crud, ids: set) -> None:
    async with AsyncSessionLocal() as session:
        service = crud(session)
        delete_ids = {menu.id for menu in await service.get()} - ids
        if delete_ids:
            for id in delete_ids:
                await service.delete(id=id)


async def load_data() -> str:
    menu_ids, submenu_ids, dish_ids = set(), set(), set()
    for row in load_workbook(filename=FILE_PATH)['Лист1'].values:
        if row[0] is not None:
            menu = await _dealer(MenuCRUD, title=row[1], description=row[2])
            menu_ids.add(menu.id)
        elif row[1] is not None:
            submenu = await _dealer(SubmenuCRUD, title=row[2], description=row[3], menu_id=menu.id)
            submenu_ids.add(submenu.id)
        else:
            dish = await _dealer(DishCRUD, title=row[3], description=row[4], price=str(row[5]), submenu_id=submenu.id)
            dish_ids.add(dish.id)
    await clean_repo(MenuCRUD, menu_ids)
    await clean_repo(SubmenuCRUD, submenu_ids)
    await clean_repo(DishCRUD, dish_ids)
    redis: aioredis.Redis = get_aioredis()
    await redis.flushall()
    return 'Data loading accomplished.'


async def task() -> str | dict[str, str] | None:
    if not is_modified():
        return 'Меню не изменялось. Выход из фоновой задачи...'
    return await load_data()
