import uuid
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

# import pickle
from app.celery_tasks.utils import get_discount_from_cache
from app.schemas.validators import price_gte_zero_validator

# from packages.generic_cache_repo.dependencies import get_redis


# constants for examples
TITLE = 'My menu/submenu/dish #1'
DESCRIPTION = 'My menu/submenu/dish description #1'
PRICE = '12.50'


# --- MIXINS ---
class TitleDescriptionMixin(BaseModel):
    title: str = Field(max_length=256, examples=[TITLE])
    description: str = Field(max_length=2000, examples=[DESCRIPTION])


class TitleDescriptionPatchMixin(BaseModel):
    title: str | None = Field(None, max_length=256, example=TITLE)
    description: str | None = Field(None, max_length=2000, examples=[DESCRIPTION])


class PriceMixin(BaseModel):
    price: str = Field(examples=[PRICE])

    @field_validator('price')
    def validate_price_gte_zero(cls, value: str) -> str:
        return price_gte_zero_validator(value)


class PricePatchMixin(BaseModel):
    price: str | None = Field(None, examples=[PRICE])

    @field_validator('price')
    def validate_price_gte_zero(cls, value: str) -> str:
        return price_gte_zero_validator(value)


# --- CREATE ---
class MenuIn(TitleDescriptionMixin):
    pass


class SubmenuIn(TitleDescriptionMixin):
    pass


class DishIn(TitleDescriptionMixin, PriceMixin):
    pass


# -- PATCH --
class MenuPatch(TitleDescriptionPatchMixin):
    pass


class SubmenuPatch(TitleDescriptionPatchMixin):
    pass


class DishPatch(TitleDescriptionPatchMixin, PricePatchMixin):
    pass


# --- OUT ---
class BaseOut(BaseModel):
    id: uuid.UUID
    model_config = ConfigDict(arbitrary_types_allowed=True,
                              from_attributes=True)


class MenuOut(BaseOut, MenuIn):
    submenus_count: int = Field(default=0)
    dishes_count: int = Field(default=0)


class SubmenuOut(BaseOut, SubmenuIn):
    dishes_count: int = Field(default=0)


class DishOut(BaseOut, TitleDescriptionMixin):
    price: str = Field(examples=[PRICE])

    @model_validator(mode='after')
    def apply_discount_(self) -> 'DishOut':
        discount = get_discount_from_cache().get(self.id, 0)
        if discount > 100:
            discount = 100
        p = float(self.price.replace(',', '.')) * (100 - discount) / 100
        self.price = str(round(Decimal(p), 2))
        return self


class Delete(BaseModel):
    status: bool = True
    message: str = Field('The item has been deleted')


class SubmenuJoined(BaseOut, SubmenuIn):
    dishes: list[DishOut]


class FullList(BaseOut, MenuIn):
    submenus: list[SubmenuJoined]
