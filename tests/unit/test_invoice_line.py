import pytest

from domain.entities.invoice_line import InvoiceLine


def test_invoice_line_can_be_created() -> None:
    line = InvoiceLine(
        product_id=1,
        quantity=3,
        unit_price=500.0,
    )

    assert line.product_id == 1
    assert line.quantity == 3
    assert line.unit_price == 500.0
    assert line.subtotal == 1500.0


@pytest.mark.parametrize("product_id", [0, -1])
def test_invoice_line_rejects_invalid_product_id(product_id: int) -> None:
    with pytest.raises(
        ValueError,
        match="Invoice line product ID must be greater than zero",
    ):
        InvoiceLine(
            product_id=product_id,
            quantity=1,
            unit_price=500.0,
        )


@pytest.mark.parametrize("quantity", [0, -1])
def test_invoice_line_rejects_invalid_quantity(quantity: int) -> None:
    with pytest.raises(
        ValueError,
        match="Invoice line quantity must be greater than zero",
    ):
        InvoiceLine(
            product_id=1,
            quantity=quantity,
            unit_price=500.0,
        )


def test_invoice_line_rejects_negative_unit_price() -> None:
    with pytest.raises(
        ValueError,
        match="Invoice line unit price cannot be negative",
    ):
        InvoiceLine(
            product_id=1,
            quantity=1,
            unit_price=-1.0,
        )
