from sqlalchemy import UUID, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Menu(Base):
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


class Submenu(Base):
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


class Dish(Base):
    submenu_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey('submenu.id'))
    submenu: Mapped['Submenu'] = relationship(back_populates='dishes')
    price: Mapped[str] = mapped_column(default='0')

    def __repr__(self) -> str:
        return f'{super().__repr__()}price: {self.price}\n'
