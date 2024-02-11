from typing import Callable, Generic

from fastapi import BackgroundTasks

from packages.generic_cache_repo.types import CacheType
from packages.generic_db_repo.types import ModelType, RepoType


class BaseService(Generic[CacheType, RepoType]):
    """Base abstract service class."""

    def __init__(self,
                 db: RepoType,
                 redis: CacheType,
                 bg_tasks: BackgroundTasks | None = None) -> None:
        self.db = db
        self.cache = redis
        self.bg_tasks = bg_tasks

    async def set_cache_on_create(self, obj: ModelType) -> None:
        pass

    async def set_cache_on_update(self, obj: dict, cache_obj: dict) -> None:
        for key in obj:
            if cache_obj[key] != obj[key]:
                cache_obj[key] = obj[key]
        await self.cache.set(cache_obj)

    async def set_cache_on_delete(self, obj: ModelType) -> None:
        await self.cache.delete(obj)

    async def _add_bg_task_or_execute(self, func: Callable, *args, **kwargs) -> None:
        """Executes the `func` either in background or directly depending on self.bg_task attribute."""
        (self.bg_tasks.add_task(func, *args, **kwargs)
         if isinstance(self.bg_tasks, BackgroundTasks)
         else await func(*args, **kwargs))

    async def _refresh(
            self, exception: bool = False, **kwargs) -> ModelType | list[ModelType]:
        """Gets result from DB. Sets the cache in background. Returns result."""
        entity = await self.db.get(exception=exception, **kwargs)
        if entity:
            await self._add_bg_task_or_execute(self.cache.set, entity)
        return entity  # type: ignore [return-value]

    async def get(self, exception: bool = False, **kwargs) -> ModelType | list[ModelType]:
        """Gets result from cache or from db if cache is None. Sets the cache in background if necessary and
           returns result."""
        return (await self.cache.get(key=kwargs.get('id')) or  # noqa
                await self._refresh(exception=exception, **kwargs))

    async def create(self, **kwargs) -> ModelType:
        """Creates the object in db and sets the cache in background."""
        obj = await self.db.create(**kwargs)
        await self._refresh(id=obj.id)
        await self._add_bg_task_or_execute(self.set_cache_on_create, obj)
        return obj

    async def update(self, **kwargs) -> ModelType:
        """Updates the object in db and sets the cache in background."""
        obj = await self.db.update(**kwargs)
        cache_obj = await self.cache.get(obj.id)
        if cache_obj:
            await self._add_bg_task_or_execute(self.set_cache_on_update, obj._asdict(), cache_obj)
        else:
            await self._refresh(id=obj.id)
        return obj

    async def delete(self, **kwargs) -> ModelType:
        """Deletes the object in db and sets the cache in background."""
        obj = await self.db.delete(**kwargs)
        await self._add_bg_task_or_execute(self.set_cache_on_delete, obj)
        return obj
