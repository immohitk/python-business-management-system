from unittest.mock import Mock, patch

from application.invoice.presentation import (
    CustomerPresentation,
    InvoiceLinePresentation,
    InvoicePresentation,
)
from presentation.cli.invoices import (
    create_invoice_creation_service,
    create_invoice_from_sale,
    create_invoice_presentation_service,
    handle_invoices,
    show_invoice,
)


def create_invoice_presentation() -> InvoicePresentation:
    return InvoicePresentation(
        invoice_number="INV-000001",
        invoice_date="2026-09-25",
        sale_id=10,
        customer=CustomerPresentation(
            name="XYZ Enterprises",
            address="45 MG Road, Bengaluru",
            phone="9876543210",
            email="xyz@example.com",
        ),
        lines=[
            InvoiceLinePresentation(
                product_name="Laptop",
                sku="LAP-001",
                quantity=2,
                unit_price=50000.0,
                amount=100000.0,
            ),
        ],
        total_amount=100000.0,
    )


def test_create_invoice_presentation_service_builds_service():
    service, connection = create_invoice_presentation_service()

    try:
        assert service.invoice_repository is not None
        assert service.sale_repository is not None
        assert service.customer_repository is not None
        assert service.product_repository is not None
        assert service.invoice_repository.connection is connection
    finally:
        connection.close()


@patch("presentation.cli.invoices.create_invoice_presentation_service")
def test_handle_invoices_back(mock_create_service):
    service = Mock()
    connection = Mock()
    mock_create_service.return_value = service, connection

    with patch("builtins.input", return_value="0"):
        handle_invoices()

    mock_create_service.assert_called_once()
    connection.close.assert_called_once()


def test_handle_invoices_accepts_injected_service():
    service = Mock()

    with patch("builtins.input", side_effect=["0"]):
        handle_invoices(service)


def test_show_invoice_prints_formatted_invoice(capsys):
    service = Mock()
    service.get_invoice_presentation.return_value = create_invoice_presentation()

    with patch("builtins.input", return_value="1"):
        show_invoice(service)

    captured = capsys.readouterr()

    assert "Show Invoice" in captured.out
    assert "TAX INVOICE" in captured.out
    assert "INV-000001" in captured.out
    assert "XYZ Enterprises" in captured.out
    assert "Laptop" in captured.out
    assert "100000.00" in captured.out
    service.get_invoice_presentation.assert_called_once_with(1)


def test_show_invoice_handles_missing_invoice(capsys):
    service = Mock()
    service.get_invoice_presentation.side_effect = ValueError(
        "Invoice not found"
    )

    with patch("builtins.input", return_value="1"):
        show_invoice(service)
    captured = capsys.readouterr()

    assert "Invoice not found" in captured.out


def test_show_invoice_handles_invalid_invoice_id(capsys):
    service = Mock()

    with patch("builtins.input", return_value="invalid"):
        show_invoice(service)

    captured = capsys.readouterr()

    assert "invalid literal" in captured.out
    service.get_invoice_presentation.assert_not_called()


def test_handle_invoices_shows_invoice(capsys):
    service = Mock()
    service.get_invoice_presentation.return_value = create_invoice_presentation()

    with patch(
        "builtins.input",
        side_effect=["2", "1", "0"],
    ):
        handle_invoices(service)

    captured = capsys.readouterr()

    assert "Invoices" in captured.out
    assert "Show Invoice" in captured.out
    assert "INV-000001" in captured.out
    assert "Laptop" in captured.out
    service.get_invoice_presentation.assert_called_once_with(1)


def test_handle_invoices_handles_invalid_choice(capsys):
    service = Mock()

    with patch(
        "builtins.input",
        side_effect=["invalid", "0"],
    ):
        handle_invoices(service)

    captured = capsys.readouterr()

    assert "Invalid choice. Please select a valid option." in captured.out


def test_create_invoice_creation_service_builds_service():
    service, connection = create_invoice_creation_service()

    try:
        assert service.sale_repository is not None
        assert service.invoice_service is not None
        assert service.invoice_service.invoice_repository is not None
        assert service.sale_repository.connection is connection
        assert service.invoice_service.invoice_repository.connection is connection
    finally:
        connection.close()


def test_create_invoice_from_sale(capsys):
    service = Mock()
    invoice = Mock()
    invoice.invoice_number = "INV-000001"
    service.create_invoice_for_sale.return_value = invoice

    with patch("builtins.input", return_value="10"):
        create_invoice_from_sale(service)

    captured = capsys.readouterr()

    assert "Create Invoice From Sale" in captured.out
    assert "Invoice created successfully: INV-000001" in captured.out
    service.create_invoice_for_sale.assert_called_once_with(10)


def test_create_invoice_from_sale_handles_missing_sale(capsys):
    service = Mock()
    service.create_invoice_for_sale.side_effect = ValueError(
        "Sale not found"
    )

    with patch("builtins.input", return_value="999"):
        create_invoice_from_sale(service)

    captured = capsys.readouterr()

    assert "Sale not found" in captured.out
    service.create_invoice_for_sale.assert_called_once_with(999)


def test_create_invoice_from_sale_handles_invalid_sale_id(capsys):
    service = Mock()

    with patch("builtins.input", return_value="invalid"):
        create_invoice_from_sale(service)

    captured = capsys.readouterr()

    assert "invalid literal" in captured.out
    service.create_invoice_for_sale.assert_not_called()


def test_handle_invoices_creates_invoice_from_sale(capsys):
    service = Mock()
    invoice_creation_service = Mock()

    invoice = Mock()
    invoice.invoice_number = "INV-000001"
    invoice_creation_service.create_invoice_for_sale.return_value = invoice

    with patch(
        "builtins.input",
        side_effect=["1", "10", "0"],
    ):
        handle_invoices(
            service=service,
            invoice_creation_service=invoice_creation_service,
        )

    captured = capsys.readouterr()

    assert "Create Invoice From Sale" in captured.out
    assert "Invoice created successfully: INV-000001" in captured.out
    invoice_creation_service.create_invoice_for_sale.assert_called_once_with(10)
