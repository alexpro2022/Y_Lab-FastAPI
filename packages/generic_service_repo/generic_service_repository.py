"""
This is a base service class implementation.
Please override set_cache_on_xxx methods with extra logic for Redis in the inherited class.
    * xxx - create/update/delete
"""
from typing import Callable, Generic

from fastapi import BackgroundTasks

from packages.generic_cache_repo.types import CacheType, _CacheType
from packages.generic_db_repo.types import ModelType, RepoType, _RepoType


class BaseService(Generic[_CacheType, _RepoType]):
    """Base abstract service class."""

    def __init__(self,
                 db: RepoType,
                 redis: CacheType,
                 bg_tasks: BackgroundTasks | None = None) -> None:
        self.db = db
        self.cache = redis
        self.bg_tasks = bg_tasks

    async def _add_bg_task_or_execute(self, method: Callable, entity: ModelType | list[ModelType]) -> None:
        self.bg_tasks.add_task(method, entity) if self.bg_tasks is not None else await method(entity)

    async def get(self, exception: bool = False, **kwargs) -> ModelType | list[ModelType] | None:
        entity = await self.cache.get(key=kwargs.get('id'), pattern=kwargs.get('pattern', '*'))
        if not entity:
            entity = await self.db.get(exception=exception, **kwargs)
            await self._add_bg_task_or_execute(self.cache.set, entity)
        return entity

    async def create(self, **kwargs) -> ModelType:
        obj = await self.db.create(**kwargs)
        await self._add_bg_task_or_execute(self.cache.set, obj)
        return obj

    async def update(self, **kwargs) -> ModelType:
        obj = await self.db.update(**kwargs)
        await self._add_bg_task_or_execute(self.cache.set, obj)
        return obj

    async def delete(self, **kwargs) -> ModelType:
        obj = await self.db.delete(**kwargs)
        await self._add_bg_task_or_execute(self.cache.delete, obj)
        return obj
