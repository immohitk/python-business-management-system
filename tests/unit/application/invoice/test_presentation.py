from application.invoice.presentation import (
    CustomerPresentation,
    InvoiceLinePresentation,
    InvoicePresentation,
)


def test_customer_presentation_stores_customer_details() -> None:
    customer = CustomerPresentation(
        name="XYZ Enterprises",
        address="45 MG Road, Bengaluru",
        phone="9876543210",
        email="xyz@example.com",
    )

    assert customer.name == "XYZ Enterprises"
    assert customer.address == "45 MG Road, Bengaluru"
    assert customer.phone == "9876543210"
    assert customer.email == "xyz@example.com"


def test_invoice_line_presentation_stores_line_details() -> None:
    line = InvoiceLinePresentation(
        product_name="Laptop",
        sku="LAP-001",
        quantity=2,
        unit_price=50000.0,
        amount=100000.0,
    )

    assert line.product_name == "Laptop"
    assert line.sku == "LAP-001"
    assert line.quantity == 2
    assert line.unit_price == 50000.0
    assert line.amount == 100000.0


def test_invoice_presentation_stores_invoice_details() -> None:
    customer = CustomerPresentation(
        name="XYZ Enterprises",
        address="45 MG Road, Bengaluru",
        phone="9876543210",
        email="xyz@example.com",
    )

    line = InvoiceLinePresentation(
        product_name="Laptop",
        sku="LAP-001",
        quantity=2,
        unit_price=50000.0,
        amount=100000.0,
    )

    invoice = InvoicePresentation(
        invoice_number="INV-000001",
        invoice_date="25/09/2026",
        sale_id=15,
        customer=customer,
        lines=[line],
        total_amount=100000.0,
    )

    assert invoice.invoice_number == "INV-000001"
    assert invoice.invoice_date == "25/09/2026"
    assert invoice.sale_id == 15
    assert invoice.customer == customer
    assert invoice.lines == [line]
    assert invoice.total_amount == 100000.0
