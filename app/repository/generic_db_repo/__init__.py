from typing import TypeVar

from pydantic import BaseModel
from sqlalchemy import orm


class Base(orm.DeclarativeBase):
    pass


ModelType = TypeVar('ModelType', bound=Base)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseModel)
