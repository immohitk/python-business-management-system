from application.invoice.formatter import InvoiceFormatter
from application.invoice.presentation import (
    CustomerPresentation,
    InvoiceLinePresentation,
    InvoicePresentation,
)


def create_invoice() -> InvoicePresentation:
    customer = CustomerPresentation(
        name="XYZ Enterprises",
        address="45 MG Road, Bengaluru",
        phone="9876543210",
        email="xyz@example.com",
    )

    lines = [
        InvoiceLinePresentation(
            product_name="Laptop",
            sku="LAP-001",
            quantity=2,
            unit_price=50000.0,
            amount=100000.0,
        ),
        InvoiceLinePresentation(
            product_name="Mouse",
            sku="MOU-001",
            quantity=5,
            unit_price=1000.0,
            amount=5000.0,
        ),
    ]

    return InvoicePresentation(
        invoice_number="INV-000001",
        invoice_date="25/09/2026",
        sale_id=15,
        customer=customer,
        lines=lines,
        total_amount=105000.0,
    )


def test_formatter_includes_invoice_information() -> None:
    invoice = create_invoice()

    output = InvoiceFormatter().format(invoice)

    assert "TAX INVOICE" in output
    assert "INV-000001" in output
    assert "25/09/2026" in output
    assert "Sale ID     : 15" in output


def test_formatter_includes_customer_information() -> None:
    invoice = create_invoice()

    output = InvoiceFormatter().format(invoice)

    assert "XYZ Enterprises" in output
    assert "45 MG Road, Bengaluru" in output
    assert "9876543210" in output
    assert "xyz@example.com" in output


def test_formatter_includes_invoice_lines_and_total() -> None:
    invoice = create_invoice()

    output = InvoiceFormatter().format(invoice)

    assert "Laptop" in output
    assert "LAP-001" in output
    assert "2" in output
    assert "50000.00" in output
    assert "100000.00" in output

    assert "Mouse" in output
    assert "MOU-001" in output
    assert "5" in output
    assert "1000.00" in output
    assert "5000.00" in output

    assert "105000.00" in output


def test_formatter_shows_dash_for_missing_customer_details() -> None:
    invoice = create_invoice()
    invoice.customer.address = None
    invoice.customer.phone = None
    invoice.customer.email = None

    output = InvoiceFormatter().format(invoice)

    assert "Address : -" in output
    assert "Phone   : -" in output
    assert "Email   : -" in output