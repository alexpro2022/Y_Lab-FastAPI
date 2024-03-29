import logging
import pickle
import uuid

from fastapi import HTTPException
from redis import asyncio as aioredis  # type: ignore [import]

from app.celery_tasks.wb_loaders import google_load_workbook, local_load_workbook
from app.core import settings
from app.models.models import Dish, Menu, Submenu
from app.repositories.db_repository import DishCRUD, MenuCRUD, SubmenuCRUD
from packages.generic_cache_repo.dependencies import get_aioredis, get_redis
from packages.generic_db_repo.dependencies import AsyncSessionLocal
from packages.generic_db_repo.types import ModelType, RepoType

logging.basicConfig(level=logging.INFO)

DISCOUNTS = 'discounts'


async def _dealer(crud: type[RepoType], **kwargs) -> ModelType:
    async with AsyncSessionLocal() as session:
        service = crud(session)
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


async def clean_repo(crud: type[RepoType], ids: set) -> None:
    async with AsyncSessionLocal() as session:
        service = crud(session)
        delete_ids = {menu.id for menu in await service.get()} - ids  # type: ignore
        if delete_ids:
            for id in delete_ids:
                await service.delete(id=id)


async def load_data() -> str:
    discounts = {}
    menu_ids, submenu_ids, dish_ids = set(), set(), set()
    if settings.google_sheets:
        rows = await google_load_workbook()
    else:
        rows = local_load_workbook()
    for row in rows:
        if row[0]:
            menu: Menu = await _dealer(MenuCRUD, title=row[1], description=row[2])
            menu_ids.add(menu.id)  # type: ignore
        elif row[1]:
            # type: ignore
            submenu: Submenu = await _dealer(SubmenuCRUD, title=row[2], description=row[3], menu_id=menu.id)
            submenu_ids.add(submenu.id)  # type: ignore
        else:
            assert submenu.id
            dish: Dish = await _dealer(
                DishCRUD, title=row[3], description=row[4], price=str(row[5]), submenu_id=submenu.id)  # type: ignore
            dish_ids.add(dish.id)  # type: ignore
            try:
                discounts[dish.id] = int(row[6])  # type: ignore
            except (IndexError, TypeError, ValueError):
                discounts[dish.id] = 0  # type: ignore

    await clean_repo(MenuCRUD, menu_ids)
    await clean_repo(SubmenuCRUD, submenu_ids)
    await clean_repo(DishCRUD, dish_ids)
    redis: aioredis.Redis = get_aioredis()
    await redis.flushall()
    await redis.set(DISCOUNTS, pickle.dumps(discounts))
    return 'Data loading accomplished.'


def get_discount_from_cache() -> dict[uuid.UUID, int]:
    return pickle.loads(get_redis().get(DISCOUNTS))
