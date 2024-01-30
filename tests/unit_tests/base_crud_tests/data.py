from datetime import datetime as dt

from pydantic import BaseModel
from sqlalchemy.orm import Mapped, mapped_column

from packages.generic_db_repo.base import Base
from packages.generic_db_repo.generic_db_repository import CRUDBaseRepository


class BaseTest(Base):
    __abstract__ = True


class Model(BaseTest):
    title: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str]
    optional_field: Mapped[dt | None]


class SchemaCreate(BaseModel):
    title: str
    description: str


class SchemaUpdate(BaseModel):
    title: str | None
    description: str | None


class Data:
    model = Model
    create_schema = SchemaCreate
    update_schema = SchemaUpdate
    field_names = ('id', 'title', 'description', 'optional_field')
    create_payload = {'title': 'My created object', 'description': 'My created object description'}
    update_payload = {'title': 'My updated object', 'description': 'My updated object description'}


class CRUD(CRUDBaseRepository):
    is_delete_allowed_not_in_use = True
    is_update_allowed_not_in_use = True