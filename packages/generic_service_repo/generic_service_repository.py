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

    async def _add_bg_task_or_execute(self, func: Callable, *args, **kwargs) -> None:
        (self.bg_tasks.add_task(func, *args, **kwargs)
         if isinstance(self.bg_tasks, BackgroundTasks)
         else await func(*args, **kwargs))

    async def refresh(self, exception: bool = False, **kwargs) -> ModelType | list[ModelType]:
        obj = await self.db.get(exception=exception, **kwargs)
        # await self.cache.set(obj)
        await self._add_bg_task_or_execute(self.cache.set, obj)
        return obj  # type: ignore [return-value]

    async def get(self, exception: bool = False, **kwargs) -> ModelType | list[ModelType]:
        # works well: setting the cache for the first time
        return (await self.cache.get(key=kwargs.get('id'), pattern=kwargs.get('pattern', '*')) or  # noqa
                await self.refresh(exception=exception, **kwargs))

    async def create(self, **kwargs) -> ModelType:
        obj = await self.db.create(**kwargs)
        # assert not await self.__check_cache(obj)
        await self._add_bg_task_or_execute(self.set_cache_on_create, obj)
        # assert await self.__check_cache(obj)
        return obj

    async def update(self, **kwargs) -> ModelType:
        obj = await self.db.update(**kwargs)
        await self._add_bg_task_or_execute(self.set_cache_on_update, obj)
        return obj

    async def delete(self, **kwargs) -> ModelType:
        obj = await self.db.delete(**kwargs)
        # assert await self.__check_cache(obj)
        await self._add_bg_task_or_execute(self.set_cache_on_delete, obj)
        # assert not await self.__check_cache(obj)
        return obj

    async def set_cache_on_create(self, obj: ModelType) -> None:
        await self.cache.set(obj)

    async def set_cache_on_update(self, obj: ModelType) -> None:
        await self.cache.set(obj)

    async def set_cache_on_delete(self, obj: ModelType) -> None:
        await self.cache.delete(obj)


'''
    async def __show_cache(self, obj=None):
        print('=========================================')
        if obj:
            print('obj', obj)
        cache = await self.cache.get()
        print('cache', cache)

    async def __check_cache(self, obj) -> bool:
        cache = await self.cache.get(obj.id)
        if cache is not None:
            return cache.id == obj.id
        return bool(cache)

'''
