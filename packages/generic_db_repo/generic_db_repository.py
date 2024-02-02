from typing import Generic, TypeAlias, TypeVar

from fastapi import HTTPException, status
from sqlalchemy import Row, Select, exc, select
from sqlalchemy.ext.asyncio import AsyncSession

from .base import Base

ModelType = TypeVar('ModelType', bound=Base)
Response: TypeAlias = Row | ModelType


class BaseCRUD(Generic[ModelType]):
    """Базовый класс для CRUD операций произвольных моделей."""
    msg_already_exists: str = 'Object with such a unique values already exists.'
    msg_not_found: str = 'Object(s) not found.'
    is_delete_allowed_not_in_use: bool = False
    is_update_allowed_not_in_use: bool = False
    has_permission_not_in_use: bool = False

    def __init__(self, model: type[ModelType], session: AsyncSession):
        self.model = model
        self.session = session
        self.__scalars = False

    def get_statement(self, **kwargs) -> Select:
        """Override the method for custom query."""
        self.__scalars = True
        return select(self.model).filter_by(**kwargs)

    async def get(self, exception: bool = False, **kwargs) -> list[Response] | Response | None:
        statement = self.get_statement(**kwargs)
        method = self.session.scalars if self.__scalars else self.session.execute
        result = await method(statement)
        res = result.all() if kwargs.get('id') is None else result.first()
        if not res and exception:
            raise HTTPException(status.HTTP_404_NOT_FOUND, self.msg_not_found)
        return res

    async def _save(self, obj: ModelType) -> ModelType:
        """Raises `BAD_REQUEST` exception if object already exists in DB. """
        self.session.add(obj)
        try:
            await self.session.commit()
        except exc.IntegrityError as exc_info:
            await self.session.rollback()
            print(exc_info)
            raise HTTPException(status.HTTP_400_BAD_REQUEST,
                                self.msg_already_exists)
        await self.session.refresh(obj)
        return obj

    async def create(self, **kwargs) -> ModelType:
        """Creates an object with payload data.
        Params:
        kwargs - for:
            - required model create data;
            - optional relation FK (like `user_id` etc)."""
        return await self._save(self.model(**kwargs))

    async def __get_or_404(self, **kwargs) -> ModelType:
        """Needs for update and delete methods as we have to extract a whole object."""
        # statement = select(self.model).filter_by(**kwargs)
        result = await self.session.scalars(select(self.model).filter_by(**kwargs))
        obj = result.first()
        if obj is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, self.msg_not_found)
        return obj

    async def update(self, **kwargs) -> ModelType:
        """Updates the object with payload data.
        Params:
        kwargs for:
            - required `id`;
            - required model update data;
            - optional `user`(user object for permission check);
            - custom params(for update allowance)."""
        obj = await self.__get_or_404(id=kwargs.pop('id'))
        try:
            user = kwargs.pop('user')
        except KeyError:
            user = None
        self.has_permission(obj, user)
        self.is_update_allowed(obj, **kwargs)
        for key in kwargs:
            setattr(obj, key, kwargs[key])
        return await self._save(obj)

    async def delete(self, **kwargs) -> ModelType:
        """Deletes the object.
        Params:
        kwargs for:
            - required `id`;
            - optional `user`(user object for permission check)."""
        obj = await self.__get_or_404(id=kwargs.get('id'))
        self.has_permission(obj, kwargs.get('user'))
        self.is_delete_allowed(obj)
        await self.session.delete(obj)
        await self.session.commit()
        return obj

    def has_permission(self, obj: ModelType, user) -> None:
        """Check for user permission and raise exception if not allowed."""
        if not self.has_permission_not_in_use:
            raise NotImplementedError('Method `has_permission` must be implemented.')

    def is_delete_allowed(self, obj: ModelType) -> None:
        """Check for custom conditions and raise exception if not allowed."""
        if not self.is_delete_allowed_not_in_use:
            raise NotImplementedError('Method `is_delete_allowed` must be implemented.')

    def is_update_allowed(self, obj: ModelType, **update_data) -> None:
        """Check for custom conditions and raise exception if not allowed.
        Normally it means to compare existing obj data against the update_data."""
        if not self.is_update_allowed_not_in_use:
            raise NotImplementedError('Method `is_update_allowed` must be implemented.')
