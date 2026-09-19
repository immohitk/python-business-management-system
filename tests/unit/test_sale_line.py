import pytest

from domain.entities.sale_line import SaleLine


def test_valid_sale_line_can_be_created():
    sale_line = SaleLine(
        product_id=1,
        quantity=2,
        unit_price=1500.0,
    )

    assert sale_line.product_id == 1
    assert sale_line.quantity == 2
    assert sale_line.unit_price == 1500.0


def test_sale_line_product_id_must_be_greater_than_zero():
    with pytest.raises(
        ValueError,
        match="Sale line product ID must be greater than zero",
    ):
        SaleLine(
            product_id=0,
            quantity=2,
            unit_price=1500.0,
        )


def test_sale_line_quantity_must_be_greater_than_zero():
    with pytest.raises(
        ValueError,
        match="Sale line quantity must be greater than zero",
    ):
        SaleLine(
            product_id=1,
            quantity=0,
            unit_price=1500.0,
        )


def test_sale_line_quantity_cannot_be_negative():
    with pytest.raises(
        ValueError,
        match="Sale line quantity must be greater than zero",
    ):
        SaleLine(
            product_id=1,
            quantity=-1,
            unit_price=1500.0,
        )


def test_sale_line_unit_price_cannot_be_negative():
    with pytest.raises(
        ValueError,
        match="Sale line unit price cannot be negative",
    ):
        SaleLine(
            product_id=1,
            quantity=2,
            unit_price=-100.0,
        )


def test_sale_line_allows_zero_unit_price():
    sale_line = SaleLine(
        product_id=1,
        quantity=2,
        unit_price=0,
    )

    assert sale_line.unit_price == 0
