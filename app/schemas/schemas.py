from decimal import Decimal
from typing import Generic

# from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.models.models import uuid_str

# constants for examples
TITLE = 'My menu/submenu/dish #1'
DESCRIPTION = 'My menu/submenu/dish description #1'
PRICE = '12.50'


class IdMixin(Generic[uuid_str], BaseModel):
    id: uuid_str
    model_config = ConfigDict(arbitrary_types_allowed=True,
                              from_attributes=True)


class TitleDescriptionMixin(BaseModel):
    title: str = Field(max_length=256, example=TITLE)
    description: str = Field(max_length=2000, example=DESCRIPTION)


class DishIn(TitleDescriptionMixin):
    price: str = Field(example=PRICE)
    # price: Decimal = Field(decimal_places=3)

    @field_validator('price')
    def validate_price_gte_zero(cls, price: str):
        p = round(Decimal(price), 2)
        if p < 0:
            raise ValueError('Цена не может быть отрицательной.')
        return str(p)


class DishOut(IdMixin, TitleDescriptionMixin):
    price: str


class SubmenuIn(TitleDescriptionMixin):
    pass


class SubmenuOut(IdMixin, SubmenuIn):
    dishes_count: int


class MenuIn(TitleDescriptionMixin):
    pass


class MenuOut(IdMixin, MenuIn):
    submenus_count: int
    dishes_count: int
