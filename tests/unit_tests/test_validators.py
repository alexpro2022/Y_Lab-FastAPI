import pytest

from app.schemas.validators import price_gte_zero_validator


@pytest.mark.parametrize('price', (
    12, '12', 14.5311, '14.5311',
))
def test_price_gte_zero_validator_returns_value(price) -> None:
    price = price_gte_zero_validator(price)
    assert isinstance(price, str)
    assert len(price.split('.')[1]) == 2


@pytest.mark.parametrize('price', (-12, '-12'))
def test_price_gte_zero_validator_raises_exc(price) -> None:
    with pytest.raises(ValueError, match='Цена не может быть отрицательной.'):
        price_gte_zero_validator(price)
