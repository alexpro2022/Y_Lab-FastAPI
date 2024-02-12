import uuid

from sqlalchemy import UUID, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from packages.generic_db_repo.base import Base


class Common(Base):
    __abstract__ = True

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(256), unique=True, index=True)
    description: Mapped[str] = mapped_column(String(2000), unique=True, index=True)

    def __repr__(self) -> str:
        return (f'\nid: {self.id}'
                f'\ntitle: {self.title}'
                f'\ndescription: {self.description}\n')


class Menu(Common):
    submenus: Mapped[list['Submenu']] = relationship(back_populates='menu', cascade='all, delete-orphan')


class Submenu(Common):
    menu_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('menu.id'))
    menu: Mapped['Menu'] = relationship(back_populates='submenus')
    dishes: Mapped[list['Dish']] = relationship(back_populates='submenu', cascade='all, delete-orphan')


class Dish(Common):
    submenu_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('submenu.id'))
    submenu: Mapped['Submenu'] = relationship(back_populates='dishes')
    price: Mapped[str] = mapped_column(default='0')

    def __repr__(self) -> str:
        return f'{super().__repr__()}price: {self.price}\n'
