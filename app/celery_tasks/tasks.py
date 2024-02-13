import asyncio

from app.celery_tasks.celery_app import app as celery
from app.celery_tasks.utils import is_modified, load_data


async def task() -> str | dict[str, str] | None:
    if not is_modified():
        return 'Меню не изменялось. Выход из фоновой задачи...'
    return await load_data()


@celery.task
def synchronize():
    return asyncio.get_event_loop().run_until_complete(task())
