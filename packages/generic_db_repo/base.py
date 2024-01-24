from typing import TypeVar
from uuid import uuid4

from pydantic import BaseModel
from sqlalchemy import UUID, MetaData, Uuid
from sqlalchemy.orm import (DeclarativeBase, Mapped, declared_attr,
                            mapped_column)


class Base(DeclarativeBase):
    metadata = MetaData(naming_convention={
        'ix': 'ix_%(column_0_label)s',
        'uq': 'uq_%(table_name)s_%(column_0_name)s',
        'ck': 'ck_%(table_name)s_%(constraint_name)s',
        'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
        'pk': 'pk_%(table_name)s',
    })

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id: Mapped[UUID | str] = mapped_column(Uuid(), primary_key=True, default=uuid4)
    # id: Mapped[str] = mapped_column(Uuid(as_uuid=False, native_uuid=True),
    #                                 primary_key=True, default=lambda: str(uuid4()))

    def __repr__(self) -> str:
        return f'\nid: {self.id}'


ModelType = TypeVar('ModelType', bound=Base)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseModel)
