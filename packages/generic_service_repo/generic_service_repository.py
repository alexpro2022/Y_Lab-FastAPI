"""
This is a base service class implementation.
Please override set_cache_on_xxx methods with extra logic for Redis in the inherited class.
    * xxx - create/update/delete
"""
from typing import Callable

from fastapi import BackgroundTasks
from package.generic_cache_repo.generic_cache_repository import BaseRedis
from package.generic_db_repo.generic_db_repository import BaseCRUD, ModelType


class BaseService:
    """Base abstract service class."""
    msg_not_impemented = "Method or function hasn't been implemented yet."

    def __init__(self,
                 db: BaseCRUD,
                 redis: BaseRedis,
                 bg_tasks: BackgroundTasks | None = None) -> None:
        self.db = db
        self.cache = redis
        self.bg_tasks = bg_tasks

    async def _add_bg_task_or_execute(self, method: Callable, entity: ModelType | list[ModelType]) -> None:
        self.bg_tasks.add_task(method, entity) if self.bg_tasks is not None else await method(entity)

    async def get(self, exception: bool = False, **kwargs) -> ModelType | list[ModelType] | None:
        entity = await self.cache.get(key=kwargs.get('id'))
        if not entity:
            entity = await self.db.get(exception=exception, **kwargs)  # if pk else await self.db.get(exception)
            await self._add_bg_task_or_execute(self.cache.set, entity)
        return entity

    async def create(self, **kwargs) -> ModelType:  # payload: BaseModel,
        """Base class provides database `create` method and
           not implemented `set_cache_on_create` template-method in FastAPI BackgroundTasks or directly."""
        obj = await self.db.create(**kwargs)
        await self._add_bg_task_or_execute(self.set_cache_on_create, obj)
        return obj

    async def update(self, **kwargs) -> ModelType:
        """Base class provides database `update` method and
           not implemented `set_cache_on_update` template-method in FastAPI BackgroundTasks or directly."""
        obj = await self.db.update(**kwargs)
        await self._add_bg_task_or_execute(self.set_cache_on_update, obj)
        return obj

    async def delete(self, **kwargs) -> ModelType:
        """Base class provides database `delete` method and
           not implemented `set_cache_on_delete` template-method in FastAPI BackgroundTasks or directly."""
        obj = await self.db.delete(**kwargs)
        await self._add_bg_task_or_execute(self.set_cache_on_delete, obj)
        return obj

    async def set_cache_on_create(self, obj: ModelType) -> None:
        raise NotImplementedError(self.msg_not_impemented)

    async def set_cache_on_update(self, obj: ModelType) -> None:
        raise NotImplementedError(self.msg_not_impemented)

    async def set_cache_on_delete(self, obj: ModelType) -> None:
        raise NotImplementedError(self.msg_not_impemented)
