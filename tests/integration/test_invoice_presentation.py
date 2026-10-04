from pathlib import Path

from application.invoice.formatter import InvoiceFormatter
from application.services.invoice_presentation_service import (
    InvoicePresentationService,
)
from application.services.invoice_service import InvoiceService
from application.services.sale_invoice_service import SaleInvoiceService
from application.services.inventory_service import InventoryService
from application.services.sale_service import SaleService
from application.services.sale_calculation_service import SaleCalculationService
from application.services.tax_charge_calculator import TaxChargeCalculator
from domain.entities.customer import Customer
from domain.entities.invoice import Invoice
from domain.entities.product import Product
from domain.entities.sale import Sale
from domain.entities.sale_item import SaleItem
from domain.entities.sale_line import SaleLine
from infrastructure.database.connection import get_connection
from infrastructure.database.initialization import initialize_database
from infrastructure.repositories.customer_repository import CustomerRepository
from infrastructure.repositories.invoice_repository import InvoiceRepository
from infrastructure.repositories.product_repository import ProductRepository
from infrastructure.repositories.sale_repository import SaleRepository
from infrastructure.repositories.stock_movement_repository import (
    StockMovementRepository,
)
from infrastructure.repositories.tax_charge_repository import TaxChargeRepository


def create_test_environment(
    tmp_path: Path,
) -> tuple[
    InvoicePresentationService,
    InvoiceFormatter,
    InvoiceRepository,
    SaleRepository,
    CustomerRepository,
    ProductRepository,
    object,
]:
    database_path = tmp_path / "test.db"
    initialize_database(database_path)
    connection = get_connection(database_path)

    invoice_repository = InvoiceRepository(connection)
    sale_repository = SaleRepository(connection)
    customer_repository = CustomerRepository(connection)
    product_repository = ProductRepository(connection)

    service = InvoicePresentationService(
        invoice_repository=invoice_repository,
        sale_repository=sale_repository,
        customer_repository=customer_repository,
        product_repository=product_repository,
    )

    formatter = InvoiceFormatter()

    return (
        service,
        formatter,
        invoice_repository,
        sale_repository,
        customer_repository,
        product_repository,
        connection,
    )


def test_invoice_presentation_integrates_with_database(
    tmp_path: Path,
):
    (
        service,
        formatter,
        invoice_repository,
        sale_repository,
        customer_repository,
        product_repository,
        connection,
    ) = create_test_environment(tmp_path)

    try:
        customer = Customer(
            id=None,
            name="XYZ Enterprises",
            phone="9876543210",
            email="xyz@example.com",
            address="45 MG Road, Bengaluru",
            created_at="2026-09-25T10:00:00",
        )
        customer_repository.add(customer)

        laptop = Product(
            id=None,
            name="Laptop",
            description="Business laptop",
            sku="LAP-001",
            price=50000.0,
            quantity=10,
            created_at="2026-09-25T09:00:00",
        )
        mouse = Product(
            id=None,
            name="Mouse",
            description="Wireless mouse",
            sku="MOU-001",
            price=1000.0,
            quantity=20,
            created_at="2026-09-25T09:00:00",
        )

        product_repository.add(laptop)
        product_repository.add(mouse)

        sale = Sale(
            id=None,
            customer_id=customer.id,
            sale_date="2026-09-25",
            total_amount=105000.0,
            created_at="2026-09-25T10:00:00",
        )
        sale_repository.add(sale)

        sale_repository.add_item(
            SaleItem(
                id=None,
                sale_id=sale.id,
                product_id=laptop.id,
                quantity=2,
                unit_price=50000.0,
            )
        )
        sale_repository.add_item(
            SaleItem(
                id=None,
                sale_id=sale.id,
                product_id=mouse.id,
                quantity=5,
                unit_price=1000.0,
            )
        )

        invoice = Invoice(
            id=None,
            sale_id=sale.id,
            invoice_number="INV-000001",
            invoice_date="2026-09-25",
            total_amount=105000.0,
            created_at="2026-09-25T10:05:00",
        )
        invoice_repository.add(invoice)

        presentation = service.get_invoice_presentation(invoice.id)
        output = formatter.format(presentation)

        assert "TAX INVOICE" in output
        assert "INV-000001" in output
        assert "25/09/2026" not in output
        assert "2026-09-25" in output
        assert "XYZ Enterprises" in output
        assert "45 MG Road, Bengaluru" in output
        assert "Laptop" in output
        assert "LAP-001" in output
        assert "50000.00" in output
        assert "100000.00" in output
        assert "Mouse" in output
        assert "MOU-001" in output
        assert "1000.00" in output
        assert "5000.00" in output
        assert "105000.00" in output
    finally:
        connection.close()


def test_sale_to_invoice_workflow_integrates_with_database(
    tmp_path: Path,
):
    (
        presentation_service,
        formatter,
        invoice_repository,
        sale_repository,
        customer_repository,
        product_repository,
        connection,
    ) = create_test_environment(tmp_path)

    try:
        customer = Customer(
            id=None,
            name="XYZ Enterprises",
            phone="9876543210",
            email="xyz@example.com",
            address="45 MG Road, Bengaluru",
            created_at="2026-09-25T10:00:00",
        )
        customer_repository.add(customer)

        laptop = Product(
            id=None,
            name="Laptop",
            description="Business laptop",
            sku="LAP-001",
            price=50000.0,
            quantity=10,
            created_at="2026-09-25T09:00:00",
        )
        product_repository.add(laptop)

        sale = Sale(
            id=None,
            customer_id=customer.id,
            sale_date="2026-09-25",
            total_amount=100000.0,
            created_at="2026-09-25T10:00:00",
        )
        sale_repository.add(sale)

        sale_repository.add_item(
            SaleItem(
                id=None,
                sale_id=sale.id,
                product_id=laptop.id,
                quantity=2,
                unit_price=50000.0,
            )
        )

        invoice_service = InvoiceService(invoice_repository)
        sale_invoice_service = SaleInvoiceService(
            sale_repository=sale_repository,
            invoice_service=invoice_service,
        )

        invoice = sale_invoice_service.create_invoice_for_sale(sale.id)

        assert invoice.id is not None
        assert invoice.sale_id == sale.id
        assert invoice.invoice_number == "INV-000001"
        assert invoice.invoice_date == "2026-09-25"
        assert invoice.total_amount == 100000.0

        stored_invoice = invoice_repository.get_by_id(invoice.id)

        assert stored_invoice is not None
        assert stored_invoice.invoice_number == "INV-000001"
        assert stored_invoice.sale_id == sale.id

        presentation = presentation_service.get_invoice_presentation(
            invoice.id
        )
        output = formatter.format(presentation)

        assert "TAX INVOICE" in output
        assert "INV-000001" in output
        assert "XYZ Enterprises" in output
        assert "45 MG Road, Bengaluru" in output
        assert "Laptop" in output
        assert "LAP-001" in output
        assert "50000.00" in output
        assert "100000.00" in output
    finally:
        connection.close()


def test_sale_service_to_invoice_service_workflow_integrates_with_database(
    tmp_path: Path,
):
    (
        presentation_service,
        formatter,
        invoice_repository,
        sale_repository,
        customer_repository,
        product_repository,
        connection,
    ) = create_test_environment(tmp_path)

    try:
        customer = Customer(
            id=None,
            name="Application Service Customer",
            phone="9876543210",
            email="application@example.com",
            address="Bengaluru",
            created_at="2026-09-28T10:00:00",
        )
        customer_repository.add(customer)

        product = Product(
            id=None,
            name="Application Service Product",
            description="Product for service integration",
            sku="SERVICE-INVOICE-001",
            price=1000.0,
            quantity=10,
            created_at="2026-09-28T10:00:00",
        )
        product_repository.add(product)

        stock_movement_repository = StockMovementRepository(connection)

        inventory_service = InventoryService(
            product_repository,
            stock_movement_repository,
        )

        tax_charge_repository = TaxChargeRepository(connection)

        sale_calculation_service = SaleCalculationService(
            TaxChargeCalculator()
        )

        sale_service = SaleService(
            sale_repository=sale_repository,
            inventory_service=inventory_service,
            tax_charge_repository=tax_charge_repository,
            sale_calculation_service=sale_calculation_service,
        )

        sale = Sale(
            id=None,
            customer_id=customer.id,
            sale_date="2026-09-28",
            total_amount=0.0,
            created_at="2026-09-28T11:00:00",
            lines=[
                SaleLine(
                    product_id=product.id,
                    quantity=2,
                    unit_price=1000.0,
                ),
            ],
        )

        sale_service.create_sale(sale)

        assert sale.id is not None
        assert sale.total_amount == 2000.0

        persisted_product = product_repository.get_by_id(product.id)

        assert persisted_product is not None
        assert persisted_product.quantity == 8

        invoice_service = InvoiceService(invoice_repository)

        sale_invoice_service = SaleInvoiceService(
            sale_repository=sale_repository,
            invoice_service=invoice_service,
        )

        invoice = sale_invoice_service.create_invoice_for_sale(sale.id)

        assert invoice.id is not None
        assert invoice.sale_id == sale.id
        assert invoice.invoice_number == "INV-000001"
        assert invoice.invoice_date == "2026-09-28"
        assert invoice.total_amount == 2000.0

        stored_invoice = invoice_repository.get_by_id(invoice.id)

        assert stored_invoice is not None
        assert stored_invoice.sale_id == sale.id
        assert stored_invoice.invoice_number == "INV-000001"
        assert stored_invoice.total_amount == 2000.0

        presentation = presentation_service.get_invoice_presentation(
            invoice.id
        )
        output = formatter.format(presentation)

        assert "TAX INVOICE" in output
        assert "INV-000001" in output
        assert "Application Service Customer" in output
        assert "Application Service Product" in output
        assert "SERVICE-INVOICE-001" in output
        assert "2000.00" in output

    finally:
        connection.close()
