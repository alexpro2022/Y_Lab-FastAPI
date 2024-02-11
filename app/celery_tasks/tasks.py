import asyncio

from app.celery_tasks.celery_app import app as celery
from app.celery_tasks.utils import task


@celery.task
def synchronize():
    return asyncio.get_event_loop().run_until_complete(task())
