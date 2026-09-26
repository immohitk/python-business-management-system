from dataclasses import dataclass

import pytest

from application.services.invoice_presentation_service import (
    InvoicePresentationService,
)
from domain.entities.customer import Customer
from domain.entities.invoice import Invoice
from domain.entities.product import Product
from domain.entities.sale import Sale
from domain.entities.sale_line import SaleLine


@dataclass
class FakeInvoiceRepository:
    invoice: Invoice | None

    def get_by_id(self, invoice_id: int) -> Invoice | None:
        return self.invoice


@dataclass
class FakeSaleRepository:
    sale: Sale | None

    def get_by_id(self, sale_id: int) -> Sale | None:
        return self.sale


@dataclass
class FakeCustomerRepository:
    customer: Customer | None

    def get_by_id(self, customer_id: int) -> Customer | None:
        return self.customer


@dataclass
class FakeProductRepository:
    products: dict[int, Product]

    def get_by_id(self, product_id: int) -> Product | None:
        return self.products.get(product_id)


def create_invoice() -> Invoice:
    return Invoice(
        id=1,
        sale_id=10,
        invoice_number="INV-000001",
        invoice_date="2026-09-25",
        total_amount=105000.0,
        created_at="2026-09-25T10:00:00",
    )


def create_sale() -> Sale:
    return Sale(
        id=10,
        customer_id=20,
        sale_date="2026-09-25",
        total_amount=105000.0,
        created_at="2026-09-25T10:00:00",
        lines=[
            SaleLine(
                product_id=30,
                quantity=2,
                unit_price=50000.0,
            ),
            SaleLine(
                product_id=31,
                quantity=5,
                unit_price=1000.0,
            ),
        ],
    )


def create_customer() -> Customer:
    return Customer(
        id=20,
        name="XYZ Enterprises",
        phone="9876543210",
        email="xyz@example.com",
        address="45 MG Road, Bengaluru",
        created_at="2026-09-25T10:00:00",
    )


def create_products() -> dict[int, Product]:
    return {
        30: Product(
            id=30,
            name="Laptop",
            description="Business laptop",
            sku="LAP-001",
            price=50000.0,
            quantity=10,
            created_at="2026-09-25T09:00:00",
        ),
        31: Product(
            id=31,
            name="Mouse",
            description="Wireless mouse",
            sku="MOU-001",
            price=1000.0,
            quantity=20,
            created_at="2026-09-25T09:00:00",
        ),
    }


def create_service(
    invoice=None,
    sale=None,
    customer=None,
    products=None,
) -> InvoicePresentationService:
    return InvoicePresentationService(
        invoice_repository=FakeInvoiceRepository(invoice),
        sale_repository=FakeSaleRepository(sale),
        customer_repository=FakeCustomerRepository(customer),
        product_repository=FakeProductRepository(products or {}),
    )


def test_builds_invoice_presentation():
    service = create_service(
        invoice=create_invoice(),
        sale=create_sale(),
        customer=create_customer(),
        products=create_products(),
    )

    result = service.get_invoice_presentation(1)

    assert result.invoice_number == "INV-000001"
    assert result.invoice_date == "2026-09-25"
    assert result.sale_id == 10
    assert result.customer.name == "XYZ Enterprises"
    assert result.customer.address == "45 MG Road, Bengaluru"

    assert len(result.lines) == 2

    assert result.lines[0].product_name == "Laptop"
    assert result.lines[0].sku == "LAP-001"
    assert result.lines[0].quantity == 2
    assert result.lines[0].unit_price == 50000.0
    assert result.lines[0].amount == 100000.0

    assert result.lines[1].product_name == "Mouse"
    assert result.lines[1].sku == "MOU-001"
    assert result.lines[1].quantity == 5
    assert result.lines[1].unit_price == 1000.0
    assert result.lines[1].amount == 5000.0

    assert result.total_amount == 105000.0


def test_raises_when_invoice_is_missing():
    service = create_service()

    with pytest.raises(ValueError, match="Invoice not found"):
        service.get_invoice_presentation(1)


def test_raises_when_sale_is_missing():
    service = create_service(
        invoice=create_invoice(),
    )

    with pytest.raises(ValueError, match="Sale not found for invoice"):
        service.get_invoice_presentation(1)


def test_raises_when_customer_is_missing():
    service = create_service(
        invoice=create_invoice(),
        sale=create_sale(),
    )

    with pytest.raises(ValueError, match="Customer not found for sale"):
        service.get_invoice_presentation(1)


def test_raises_when_product_is_missing():
    service = create_service(
        invoice=create_invoice(),
        sale=create_sale(),
        customer=create_customer(),
        products={
            30: create_products()[30],
        },
    )

    with pytest.raises(ValueError, match="Product not found: 31"):
        service.get_invoice_presentation(1)