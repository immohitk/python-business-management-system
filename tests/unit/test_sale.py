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


def test_sale_preserves_sale_line_data():
    first_line = SaleLine(
        product_id=1,
        quantity=2,
        unit_price=1000.0,
    )
    second_line = SaleLine(
        product_id=2,
        quantity=3,
        unit_price=500.0,
    )

    sale = Sale(
        id=None,
        customer_id=1,
        sale_date="2026-09-19",
        total_amount=3500.0,
        created_at="2026-09-19T10:00:00",
        lines=[first_line, second_line],
    )

    assert sale.lines[0].product_id == 1
    assert sale.lines[0].quantity == 2
    assert sale.lines[0].unit_price == 1000.0

    assert sale.lines[1].product_id == 2
    assert sale.lines[1].quantity == 3
    assert sale.lines[1].unit_price == 500.0


def test_sale_supports_multiple_distinct_products():
    lines = [
        SaleLine(
            product_id=1,
            quantity=1,
            unit_price=1500.0,
        ),
        SaleLine(
            product_id=2,
            quantity=2,
            unit_price=750.0,
        ),
        SaleLine(
            product_id=3,
            quantity=1,
            unit_price=250.0,
        ),
    ]

    sale = Sale(
        id=None,
        customer_id=1,
        sale_date="2026-09-19",
        total_amount=3250.0,
        created_at="2026-09-19T10:00:00",
        lines=lines,
    )

    assert [line.product_id for line in sale.lines] == [1, 2, 3]
    assert len(sale.lines) == 3


def test_invalid_sale_line_cannot_be_created_for_sale():
    with pytest.raises(
        ValueError,
        match="Sale line quantity must be greater than zero",
    ):
        SaleLine(
            product_id=1,
            quantity=0,
            unit_price=1000.0,
        )


def test_sale_calculated_total_sums_sale_line_subtotals():
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

    assert sale.calculated_total == 2400.0


def test_sale_calculated_total_supports_multiple_lines():
    lines = [
        SaleLine(
            product_id=1,
            quantity=1,
            unit_price=1500.0,
        ),
        SaleLine(
            product_id=2,
            quantity=2,
            unit_price=750.0,
        ),
        SaleLine(
            product_id=3,
            quantity=1,
            unit_price=250.0,
        ),
    ]

    sale = Sale(
        id=None,
        customer_id=1,
        sale_date="2026-09-19",
        total_amount=3250.0,
        created_at="2026-09-19T10:00:00",
        lines=lines,
    )

    assert sale.calculated_total == 3250.0


def test_sale_calculated_total_is_zero_without_sale_lines():
    sale = Sale(
        id=None,
        customer_id=1,
        sale_date="2026-09-19",
        total_amount=0.0,
        created_at="2026-09-19T10:00:00",
    )

    assert sale.calculated_total == 0.0


def test_sale_apply_calculated_total_updates_total_amount():
    sale = Sale(
        id=None,
        customer_id=1,
        sale_date="2026-09-20",
        total_amount=0.0,
        created_at="2026-09-20T10:00:00",
        lines=[
            SaleLine(product_id=1, quantity=2, unit_price=1000.0),
        ],
    )

    sale.apply_calculated_total()

    assert sale.total_amount == 2000.0


def test_sale_apply_calculated_total_supports_multiple_lines():
    sale = Sale(
        id=None,
        customer_id=1,
        sale_date="2026-09-20",
        total_amount=100.0,
        created_at="2026-09-20T10:00:00",
        lines=[
            SaleLine(product_id=1, quantity=2, unit_price=1000.0),
            SaleLine(product_id=2, quantity=1, unit_price=400.0),
        ],
    )

    sale.apply_calculated_total()

    assert sale.total_amount == 2400.0


def test_sale_apply_calculated_total_sets_zero_for_empty_sale():
    sale = Sale(
        id=None,
        customer_id=1,
        sale_date="2026-09-20",
        total_amount=500.0,
        created_at="2026-09-20T10:00:00",
    )

    sale.apply_calculated_total()

    assert sale.total_amount == 0.0


def test_sale_apply_calculated_total_does_not_modify_sale_lines():
    lines = [
        SaleLine(product_id=1, quantity=2, unit_price=1000.0),
        SaleLine(product_id=2, quantity=1, unit_price=400.0),
    ]

    sale = Sale(
        id=None,
        customer_id=1,
        sale_date="2026-09-20",
        total_amount=0.0,
        created_at="2026-09-20T10:00:00",
        lines=lines,
    )

    sale.apply_calculated_total()

    assert sale.lines == lines
    assert sale.calculated_total == 2400.0


def test_sale_calculated_total_supports_fractional_unit_prices():
    sale = Sale(
        id=None,
        customer_id=1,
        sale_date="2026-09-20",
        total_amount=0.0,
        created_at="2026-09-20T10:00:00",
        lines=[
            SaleLine(
                product_id=1,
                quantity=3,
                unit_price=199.99,
            ),
            SaleLine(
                product_id=2,
                quantity=2,
                unit_price=49.50,
            ),
        ],
    )

    assert sale.calculated_total == 698.97


def test_sale_calculated_total_requires_valid_sale_lines():
    with pytest.raises(
        ValueError,
        match="Sale line unit price cannot be negative",
    ):
        SaleLine(
            product_id=1,
            quantity=1,
            unit_price=-100.0,
        )
