from unittest.mock import Mock

import pytest

from application.services.sale_invoice_service import SaleInvoiceService
from domain.entities.sale import Sale


def create_sale() -> Sale:
    return Sale(
        id=15,
        customer_id=3,
        sale_date="2026-09-27",
        total_amount=105000.0,
        created_at="2026-09-27T10:00:00",
    )


def test_create_invoice_for_sale_creates_invoice():
    sale_repository = Mock()
    invoice_service = Mock()

    sale_repository.get_by_id.return_value = create_sale()

    expected_invoice = Mock()
    invoice_service.create_invoice.return_value = expected_invoice

    service = SaleInvoiceService(
        sale_repository=sale_repository,
        invoice_service=invoice_service,
    )

    result = service.create_invoice_for_sale(15)

    assert result is expected_invoice
    sale_repository.get_by_id.assert_called_once_with(15)
    invoice_service.create_invoice.assert_called_once()


def test_create_invoice_for_sale_uses_sale_information():
    sale_repository = Mock()
    invoice_service = Mock()

    sale_repository.get_by_id.return_value = create_sale()

    service = SaleInvoiceService(
        sale_repository=sale_repository,
        invoice_service=invoice_service,
    )

    service.create_invoice_for_sale(15)

    invoice = invoice_service.create_invoice.call_args.args[0]

    assert invoice.sale_id == 15
    assert invoice.invoice_date == "2026-09-27"
    assert invoice.total_amount == 105000.0
    assert invoice.invoice_number == "PENDING"


def test_create_invoice_for_sale_raises_when_sale_is_missing():
    sale_repository = Mock()
    invoice_service = Mock()

    sale_repository.get_by_id.return_value = None

    service = SaleInvoiceService(
        sale_repository=sale_repository,
        invoice_service=invoice_service,
    )

    with pytest.raises(ValueError, match="Sale not found"):
        service.create_invoice_for_sale(999)

    invoice_service.create_invoice.assert_not_called()
