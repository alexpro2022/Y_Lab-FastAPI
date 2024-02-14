import asyncio

from app.celery_tasks.celery_app import app as celery
from app.celery_tasks.utils import load_data
from app.celery_tasks.wb_loaders import is_modified


async def task() -> str | dict[str, str] | None:
    if not await is_modified():
        return 'Меню не изменялось. Выход из фоновой задачи...'
    return await load_data()


@celery.task
def synchronize():
    return asyncio.get_event_loop().run_until_complete(task())
