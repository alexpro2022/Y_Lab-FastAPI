from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from ...generic_db_repository import BaseCRUD


class Data:
    field_names = ('id', 'title', 'description', 'optional_field')
    create_payload = {'title': 'My created object', 'description': 'My created object description'}
    update_payload = {'title': 'My updated object', 'description': 'My updated object description'}


class TestBase(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)


# --- Models ---
class Model(TestBase):
    __tablename__ = 'model'
    title: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str]

    def __repr__(self):
        return (f'\ntitle: {self.title}'
                f'\ndescription: {self.description}'
                f'\noptional_field: {self.optional_field}')


# --- Repositories ---
class CRUDScalars(BaseCRUD):
    """Testing the BaseCRUD without hooks exceptions."""
    msg_already_exists = 'Scalars_exists.'
    msg_not_found = 'Scalars_not_found.'
    has_permission_not_in_use = True
    is_delete_allowed_not_in_use = True
    is_update_allowed_not_in_use = True

    def __init__(self, session: AsyncSession):
        super().__init__(Model, session)


class CRUDExec(BaseCRUD):
    """Testing the BaseCRUD without hooks exceptions."""
    msg_already_exists = 'Exec_exists.'
    msg_not_found = 'Exec_not_found.'
    has_permission_not_in_use = True
    is_delete_allowed_not_in_use = True
    is_update_allowed_not_in_use = True

    def __init__(self, session: AsyncSession):
        super().__init__(Model, session)

    def get_statement(self, **kwargs) -> Select:
        return select(
            self.model.id,
            self.model.title,
            self.model.description,
        ).filter_by(**kwargs)
