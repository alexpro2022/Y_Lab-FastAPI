import pytest

from app.models import Dish, Menu, Submenu
from tests.fixtures import data as d

COMMON_FIELDS = ('id', 'title', 'description')

parametrize = pytest.mark.parametrize('model, data, attrs', (
    (Dish, d.DISH_POST_PAYLOAD, (*COMMON_FIELDS, 'price')),
    (Menu, d.MENU_POST_PAYLOAD, (*COMMON_FIELDS,)),
    (Submenu, d.SUBMENU_POST_PAYLOAD, (*COMMON_FIELDS,)),
))


@parametrize
def test_model_attr(model, data: dict[str, str], attrs: str) -> None:
    for attr_name in attrs:
        assert hasattr(model, attr_name)


@parametrize
def test_model_repr(model, data: dict[str, str], attrs: str) -> None:
    representation = repr(model(**data))
    for attr_name in attrs:
        assert representation.find(attr_name) != -1
