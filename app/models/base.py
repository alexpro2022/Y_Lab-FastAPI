from uuid import uuid4

from sqlalchemy import UUID, MetaData, String
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

    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=uuid4)
    title: Mapped[str] = mapped_column(String(256), unique=True, index=True)
    description: Mapped[str] = mapped_column(String(2000))

    def __repr__(self) -> str:
        return (f'\nid: {self.id}'
                f'\ntitle: {self.title}'
                f'\ndescription: {self.description}\n')
