import pytest

from domain.entities.sale import Sale
from domain.entities.sale_line import SaleLine


def test_valid_sale_can_be_created():
    sale = Sale(
        id=None,
        customer_id=1,
        sale_date="2026-09-19",
        total_amount=2400.0,
        created_at="2026-09-19T10:00:00",
    )

    assert sale.id is None
    assert sale.customer_id == 1
    assert sale.sale_date == "2026-09-19"
    assert sale.total_amount == 2400.0
    assert sale.created_at == "2026-09-19T10:00:00"
    assert sale.lines == []


def test_sale_can_contain_sale_lines():
    lines = [
        SaleLine(
            product_id=1,
            quantity=2,
            unit_price=1000.0,
        ),
        SaleLine(
            product_id=2,
            quantity=1,
            unit_price=400.0,
        ),
    ]

    sale = Sale(
        id=None,
        customer_id=1,
        sale_date="2026-09-19",
        total_amount=2400.0,
        created_at="2026-09-19T10:00:00",
        lines=lines,
    )

    assert sale.lines == lines
    assert len(sale.lines) == 2


def test_sale_customer_id_must_be_greater_than_zero():
    with pytest.raises(
        ValueError,
        match="Sale customer ID must be greater than zero",
    ):
        Sale(
            id=None,
            customer_id=0,
            sale_date="2026-09-19",
            total_amount=2400.0,
            created_at="2026-09-19T10:00:00",
        )


def test_sale_customer_id_cannot_be_negative():
    with pytest.raises(
        ValueError,
        match="Sale customer ID must be greater than zero",
    ):
        Sale(
            id=None,
            customer_id=-1,
            sale_date="2026-09-19",
            total_amount=2400.0,
            created_at="2026-09-19T10:00:00",
        )


def test_sale_created_at_cannot_be_empty():
    with pytest.raises(
        ValueError,
        match="Sale created_at cannot be empty",
    ):
        Sale(
            id=None,
            customer_id=1,
            sale_date="2026-09-19",
            total_amount=2400.0,
            created_at="",
        )


def test_sale_created_at_cannot_be_whitespace():
    with pytest.raises(
        ValueError,
        match="Sale created_at cannot be empty",
    ):
        Sale(
            id=None,
            customer_id=1,
            sale_date="2026-09-19",
            total_amount=2400.0,
            created_at="   ",
        )


def test_sale_date_cannot_be_empty():
    with pytest.raises(
        ValueError,
        match="Sale date cannot be empty",
    ):
        Sale(
            id=None,
            customer_id=1,
            sale_date="",
            total_amount=2400.0,
            created_at="2026-09-19T10:00:00",
        )


def test_sale_date_cannot_be_whitespace():
    with pytest.raises(
        ValueError,
        match="Sale date cannot be empty",
    ):
        Sale(
            id=None,
            customer_id=1,
            sale_date="   ",
            total_amount=2400.0,
            created_at="2026-09-19T10:00:00",
        )


def test_sale_total_amount_cannot_be_negative():
    with pytest.raises(
        ValueError,
        match="Sale total amount cannot be negative",
    ):
        Sale(
            id=None,
            customer_id=1,
            sale_date="2026-09-19",
            total_amount=-1.0,
            created_at="2026-09-19T10:00:00",
        )


def test_sale_allows_zero_total_amount():
    sale = Sale(
        id=None,
        customer_id=1,
        sale_date="2026-09-19",
        total_amount=0.0,
        created_at="2026-09-19T10:00:00",
    )

    assert sale.total_amount == 0.0
