from uuid import uuid4

from sqlalchemy import UUID, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from packages.generic_db_repo.base import Base


class Common(Base):
    __abstract__ = True

    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=uuid4)
    title: Mapped[str] = mapped_column(String(256), unique=True, index=True)
    description: Mapped[str] = mapped_column(String(2000))

    def __repr__(self) -> str:
        return (f'\nid: {self.id}'
                f'\ntitle: {self.title}'
                f'\ndescription: {self.description}\n')


class Menu(Common):
    submenus: Mapped[list['Submenu']] = relationship(
        back_populates='menu',
        cascade='all, delete-orphan',
        lazy='selectin',
    )

    @property
    def submenus_count(self) -> int:
        return len(self.submenus)

    @property
    def dishes_count(self) -> int:
        return sum(submenu.dishes_count for submenu in self.submenus)

    def __repr__(self) -> str:
        return (f'{super().__repr__()}'
                f'submenus_count: {self.submenus_count}\n'
                f'dishes_count: {self.dishes_count}\n')


class Submenu(Common):
    menu_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey('menu.id'))
    menu: Mapped['Menu'] = relationship(back_populates='submenus')
    dishes: Mapped[list['Dish']] = relationship(
        back_populates='submenu',
        cascade='all, delete-orphan',
        lazy='selectin',
    )

    @property
    def dishes_count(self) -> int:
        return len(self.dishes)

    def __repr__(self) -> str:
        return f'{super().__repr__()}dishes_count: {self.dishes_count}\n'


class Dish(Common):
    submenu_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey('submenu.id'))
    submenu: Mapped['Submenu'] = relationship(back_populates='dishes')
    price: Mapped[str] = mapped_column(default='0')

    def __repr__(self) -> str:
        return f'{super().__repr__()}price: {self.price}\n'
