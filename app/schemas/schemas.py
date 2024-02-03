import uuid

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.schemas.validators import price_gte_zero_validator

# constants for examples
TITLE = 'My menu/submenu/dish #1'
DESCRIPTION = 'My menu/submenu/dish description #1'
PRICE = '12.50'


# --- MIXINS ---
class TitleDescriptionMixin(BaseModel):
    title: str = Field(max_length=256, example=TITLE)
    description: str = Field(max_length=2000, example=DESCRIPTION)


class TitleDescriptionPatchMixin(BaseModel):
    title: str | None = Field(None, max_length=256, example=TITLE)
    description: str | None = Field(None, max_length=2000, example=DESCRIPTION)


class PriceMixin(BaseModel):
    price: str = Field(example=PRICE)

    @field_validator('price')
    def validate_price_gte_zero(cls, value: str):
        return price_gte_zero_validator(value)


class PricePatchMixin(BaseModel):
    price: str | None = Field(None, example=PRICE)

    @field_validator('price')
    def validate_price_gte_zero(cls, value: str):
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
    price: str
