import asyncio

from app.celery_tasks.celery_app import app as celery
from app.celery_tasks.utils import load_data
from app.celery_tasks.wb_loaders import (
    google_get_mod_timestamp,
    is_modified,
    local_get_mod_timestamp,
)
from app.core.config import settings


async def task() -> str | dict[str, str] | None:
    if settings.google_sheets:
        timestamp = await google_get_mod_timestamp()
    else:
        timestamp = local_get_mod_timestamp()
    if not is_modified(timestamp):
        return 'Меню не изменялось. Выход из фоновой задачи...'
    return await load_data()


@celery.task
def synchronize():
    return asyncio.get_event_loop().run_until_complete(task())
