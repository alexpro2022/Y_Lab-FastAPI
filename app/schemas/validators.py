from decimal import Decimal


def price_gte_zero_validator(price: str):
    p = round(Decimal(price), 2)
    if p < 0:
        raise ValueError('Цена не может быть отрицательной.')
    return str(p)
