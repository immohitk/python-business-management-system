import pytest

from domain.entities.invoice import Invoice
from domain.entities.invoice_line import InvoiceLine


def create_valid_invoice() -> Invoice:
    return Invoice(
        id=None,
        sale_id=1,
        invoice_number="INV-001",
        invoice_date="2026-09-23",
        total_amount=1500.0,
        created_at="2026-09-23T20:00:00",
    )


def test_invoice_can_be_created() -> None:
    invoice = create_valid_invoice()

    assert invoice.id is None
    assert invoice.sale_id == 1
    assert invoice.invoice_number == "INV-001"
    assert invoice.invoice_date == "2026-09-23"
    assert invoice.total_amount == 1500.0
    assert invoice.created_at == "2026-09-23T20:00:00"


@pytest.mark.parametrize("sale_id", [0, -1])
def test_invoice_rejects_invalid_sale_id(sale_id: int) -> None:
    with pytest.raises(ValueError, match="Invoice sale ID must be greater than zero"):
        Invoice(
            id=None,
            sale_id=sale_id,
            invoice_number="INV-001",
            invoice_date="2026-09-23",
            total_amount=1500.0,
            created_at="2026-09-23T20:00:00",
        )


@pytest.mark.parametrize("invoice_date", ["", "   "])
def test_invoice_rejects_empty_invoice_date(invoice_date: str) -> None:
    with pytest.raises(ValueError, match="Invoice date cannot be empty"):
        Invoice(
            id=None,
            sale_id=1,
            invoice_number="INV-001",
            invoice_date=invoice_date,
            total_amount=1500.0,
            created_at="2026-09-23T20:00:00",
        )


def test_invoice_rejects_negative_total_amount() -> None:
    with pytest.raises(
        ValueError,
        match="Invoice total amount cannot be negative",
    ):
        Invoice(
            id=None,
            sale_id=1,
            invoice_number="INV-001",
            invoice_date="2026-09-23",
            total_amount=-1.0,
            created_at="2026-09-23T20:00:00",
        )


@pytest.mark.parametrize("created_at", ["", "   "])
def test_invoice_rejects_empty_created_at(created_at: str) -> None:
    with pytest.raises(
        ValueError,
        match="Invoice created_at cannot be empty",
    ):
        Invoice(
            id=None,
            sale_id=1,
            invoice_number="INV-001",
            invoice_date="2026-09-23",
            total_amount=1500.0,
            created_at=created_at,
        )


def test_invoice_can_calculate_total_from_lines() -> None:
    invoice = Invoice(
        id=None,
        sale_id=1,
        invoice_number="INV-001",
        invoice_date="2026-09-23",
        total_amount=0.0,
        created_at="2026-09-23T20:00:00",
        lines=[
            InvoiceLine(product_id=1, quantity=2, unit_price=500.0),
            InvoiceLine(product_id=2, quantity=1, unit_price=250.0),
        ],
    )

    assert invoice.calculated_total == 1250.0

    invoice.apply_calculated_total()

    assert invoice.total_amount == 1250.0


@pytest.mark.parametrize("invoice_number", ["", "   "])
def test_invoice_rejects_empty_invoice_number(invoice_number: str) -> None:
    with pytest.raises(ValueError, match="Invoice number cannot be empty"):
        Invoice(
            id=None,
            sale_id=1,
            invoice_number=invoice_number,
            invoice_date="2026-09-23",
            total_amount=1500.0,
            created_at="2026-09-23T20:00:00",
        )
