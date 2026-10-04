import pytest
from pathlib import Path

from application.services.customer_service import CustomerService
from application.services.product_service import ProductService
from application.services.supplier_service import SupplierService
from application.services.inventory_service import InventoryService
from application.services.sale_service import SaleService
from application.services.invoice_service import InvoiceService
from application.services.sale_invoice_service import SaleInvoiceService
from application.services.sale_calculation_service import SaleCalculationService
from application.services.tax_charge_calculator import TaxChargeCalculator
from application.services.reporting_service import ReportingService
from application.services.payment_balance_service import PaymentBalanceService
from application.services.sale_payment_service import SalePaymentService
from domain.entities.customer import Customer
from domain.entities.product import Product
from domain.entities.supplier import Supplier
from domain.entities.stock_movement import StockMovementType
from domain.entities.sale import Sale
from domain.entities.sale_line import SaleLine
from infrastructure.repositories.sale_repository import SaleRepository
from infrastructure.database.connection import get_connection
from infrastructure.database.initialization import initialize_database
from infrastructure.repositories.customer_repository import CustomerRepository
from infrastructure.repositories.product_repository import ProductRepository
from infrastructure.repositories.supplier_repository import SupplierRepository
from infrastructure.repositories.stock_movement_repository import (
    StockMovementRepository,
)
from infrastructure.repositories.invoice_repository import InvoiceRepository
from infrastructure.repositories.reporting_repository import ReportingRepository
from infrastructure.repositories.tax_charge_repository import TaxChargeRepository
from infrastructure.repositories.sale_payment_repository import SalePaymentRepository


def create_database(tmp_path: Path):
    database_path = tmp_path / "application_services.db"
    initialize_database(database_path)
    return get_connection(database_path)


def test_application_services_persist_and_retrieve_master_data(tmp_path):
    connection = create_database(tmp_path)

    try:
        product_service = ProductService(ProductRepository(connection))
        customer_service = CustomerService(CustomerRepository(connection))
        supplier_service = SupplierService(SupplierRepository(connection))

        product = Product(
            id=None,
            name="Integration Product",
            description="Product through application service",
            sku="SERVICE-001",
            price=750.0,
            quantity=20,
            created_at="2026-09-13T10:00:00",
        )

        customer = Customer(
            id=None,
            name="Integration Customer",
            phone="9876543210",
            email="customer@example.com",
            address="Delhi",
            created_at="2026-09-13T10:00:00",
        )

        supplier = Supplier(
            id=None,
            name="Integration Supplier",
            phone="9123456780",
            email="supplier@example.com",
            address="Mumbai",
            created_at="2026-09-13T10:00:00",
        )

        product_service.add_product(product)
        customer_service.add_customer(customer)
        supplier_service.add_supplier(supplier)

        assert product_service.get_product(product.id) == product
        assert customer_service.get_customer(customer.id) == customer
        assert supplier_service.get_supplier(supplier.id) == supplier

        assert product_service.get_products() == [product]
        assert customer_service.get_customers() == [customer]
        assert supplier_service.get_suppliers() == [supplier]
    finally:
        connection.close()


def test_inventory_service_persists_stock_operations(tmp_path):
    connection = create_database(tmp_path)

    try:
        product_repository = ProductRepository(connection)
        stock_movement_repository = StockMovementRepository(connection)
        inventory_service = InventoryService(
            product_repository,
            stock_movement_repository,
        )

        product = Product(
            id=None,
            name="Inventory Integration Product",
            description="Inventory service integration test",
            sku="INVENTORY-001",
            price=500.0,
            quantity=20,
            created_at="2026-09-16T10:00:00",
        )

        product_repository.add(product)

        inventory_service.stock_in(
            product.id,
            5,
            created_at="2026-09-16T11:00:00",
        )

        inventory_service.adjust_stock(
            product.id,
            12,
            created_at="2026-09-16T12:00:00",
        )

        inventory_service.stock_out(
            product.id,
            4,
            created_at="2026-09-16T13:00:00",
        )

        result = product_repository.get_by_id(product.id)

        assert result is not None
        assert result.quantity == 8

        movements = stock_movement_repository.get_movements(product.id)

        assert len(movements) == 3

        assert movements[0].movement_type == StockMovementType.ADD
        assert movements[0].quantity == 5
        assert movements[0].resulting_stock == 25
        assert movements[0].created_at == "2026-09-16T11:00:00"

        assert movements[1].movement_type == StockMovementType.ADJUST
        assert movements[1].quantity == 12
        assert movements[1].resulting_stock == 12
        assert movements[1].created_at == "2026-09-16T12:00:00"

        assert movements[2].movement_type == StockMovementType.DEDUCT
        assert movements[2].quantity == 4
        assert movements[2].resulting_stock == 8
        assert movements[2].created_at == "2026-09-16T13:00:00"
    finally:
        connection.close()


def test_inventory_service_rejects_invalid_stock_operations(tmp_path):
    connection = create_database(tmp_path)

    try:
        product_repository = ProductRepository(connection)
        stock_movement_repository = StockMovementRepository(connection)
        inventory_service = InventoryService(
            product_repository,
            stock_movement_repository,
        )

        product = Product(
            id=None,
            name="Inventory Validation Product",
            description=None,
            sku="INVENTORY-002",
            price=500.0,
            quantity=10,
            created_at="2026-09-16T10:00:00",
        )

        product_repository.add(product)

        with pytest.raises(
            ValueError,
            match="Stock addition amount must be greater than zero",
        ):
            inventory_service.stock_in(
                product.id,
                0,
                created_at="2026-09-16T11:00:00",
            )

        with pytest.raises(
            ValueError,
            match="Stock quantity cannot be negative",
        ):
            inventory_service.adjust_stock(
                product.id,
                -1,
                created_at="2026-09-16T11:00:00",
            )

        with pytest.raises(
            ValueError,
            match="Stock deduction amount must be greater than zero",
        ):
            inventory_service.stock_out(
                product.id,
                0,
                created_at="2026-09-16T11:00:00",
            )

        result = product_repository.get_by_id(product.id)

        assert result is not None
        assert result.quantity == 10
        assert stock_movement_repository.get_movements(product.id) == []
    finally:
        connection.close()


def test_inventory_service_rejects_insufficient_stock(tmp_path):
    connection = create_database(tmp_path)

    try:
        product_repository = ProductRepository(connection)
        stock_movement_repository = StockMovementRepository(connection)
        inventory_service = InventoryService(
            product_repository,
            stock_movement_repository,
        )

        product = Product(
            id=None,
            name="Insufficient Stock Product",
            description=None,
            sku="INVENTORY-003",
            price=500.0,
            quantity=10,
            created_at="2026-09-16T10:00:00",
        )

        product_repository.add(product)

        with pytest.raises(
            ValueError,
            match="Stock quantity cannot be negative",
        ):
            inventory_service.stock_out(
                product.id,
                11,
                created_at="2026-09-16T11:00:00",
            )

        result = product_repository.get_by_id(product.id)

        assert result is not None
        assert result.quantity == 10
        assert stock_movement_repository.get_movements(product.id) == []
    finally:
        connection.close()


def test_product_customer_sale_inventory_workflow_integrates_through_application_services(
    tmp_path,
):
    connection = create_database(tmp_path)

    try:
        product_repository = ProductRepository(connection)
        customer_repository = CustomerRepository(connection)
        sale_repository = SaleRepository(connection)
        stock_movement_repository = StockMovementRepository(connection)

        product_service = ProductService(product_repository)
        customer_service = CustomerService(customer_repository)

        inventory_service = InventoryService(
            product_repository,
            stock_movement_repository,
        )

        tax_charge_repository = TaxChargeRepository(connection)

        sale_calculation_service = SaleCalculationService(
            TaxChargeCalculator()
        )

        sale_payment_repository = SalePaymentRepository(connection)
        sale_payment_service = SalePaymentService(sale_payment_repository)
        payment_balance_service = PaymentBalanceService()

        sale_service = SaleService(
            sale_repository,
            inventory_service,
            tax_charge_repository,
            sale_calculation_service,
            sale_payment_service,
            payment_balance_service,
        )

        product = Product(
            id=None,
            name="Sales Integration Product",
            description="Product used in sales integration test",
            sku="SALES-INTEGRATION-001",
            price=100.0,
            quantity=0,
            created_at="2026-09-28T10:00:00",
        )

        customer = Customer(
            id=None,
            name="Sales Integration Customer",
            phone="9876543210",
            email="sales.integration@example.com",
            address="Delhi",
            created_at="2026-09-28T10:00:00",
        )

        product_service.add_product(product)
        customer_service.add_customer(customer)

        inventory_service.stock_in(
            product.id,
            10,
            created_at="2026-09-28T11:00:00",
        )

        sale = Sale(
            id=None,
            customer_id=customer.id,
            sale_date="2026-09-28",
            total_amount=0.0,
            created_at="2026-09-28T12:00:00",
            lines=[
                SaleLine(
                    product_id=product.id,
                    quantity=2,
                    unit_price=100.0,
                ),
            ],
        )

        sale_service.create_sale(sale)

        assert sale.customer_id == customer.id
        assert sale.total_amount == 200.0

        persisted_sale = sale_repository.get_by_id(sale.id)

        assert persisted_sale is not None
        assert persisted_sale.customer_id == customer.id
        assert persisted_sale.total_amount == 200.0

        persisted_product = product_repository.get_by_id(product.id)

        assert persisted_product is not None
        assert persisted_product.quantity == 8

        movements = stock_movement_repository.get_movements(product.id)

        assert len(movements) == 2
        assert movements[0].movement_type == StockMovementType.ADD
        assert movements[0].resulting_stock == 10
        assert movements[1].movement_type == StockMovementType.DEDUCT
        assert movements[1].resulting_stock == 8

    finally:
        connection.close()


def test_complete_business_workflow_integrates_all_application_services(
    tmp_path,
):
    database_path = tmp_path / "end_to_end.db"
    initialize_database(database_path)
    connection = get_connection(database_path)

    try:
        product_repository = ProductRepository(connection)
        customer_repository = CustomerRepository(connection)
        sale_repository = SaleRepository(connection)
        stock_movement_repository = StockMovementRepository(connection)
        invoice_repository = InvoiceRepository(connection)
        reporting_repository = ReportingRepository(connection)

        product_service = ProductService(product_repository)
        customer_service = CustomerService(customer_repository)

        inventory_service = InventoryService(
            product_repository,
            stock_movement_repository,
        )

        tax_charge_repository = TaxChargeRepository(connection)

        sale_calculation_service = SaleCalculationService(
            TaxChargeCalculator()
        )

        sale_payment_repository = SalePaymentRepository(connection)
        sale_payment_service = SalePaymentService(sale_payment_repository)
        payment_balance_service = PaymentBalanceService()

        sale_service = SaleService(
            sale_repository,
            inventory_service,
            tax_charge_repository,
            sale_calculation_service,
            sale_payment_service,
            payment_balance_service,
        )

        invoice_service = InvoiceService(invoice_repository)

        sale_invoice_service = SaleInvoiceService(
            sale_repository=sale_repository,
            invoice_service=invoice_service,
        )

        reporting_service = ReportingService(reporting_repository)

        product = Product(
            id=None,
            name="End-to-End Product",
            description="Complete business workflow product",
            sku="E2E-001",
            price=500.0,
            quantity=0,
            created_at="2026-09-29T10:00:00",
        )

        customer = Customer(
            id=None,
            name="End-to-End Customer",
            phone="9999999999",
            email="e2e@example.com",
            address="Bengaluru",
            created_at="2026-09-29T10:05:00",
        )

        product_service.add_product(product)
        customer_service.add_customer(customer)

        inventory_service.stock_in(
            product.id,
            10,
            created_at="2026-09-29T10:10:00",
        )

        sale = Sale(
            id=None,
            customer_id=customer.id,
            sale_date="2026-09-29",
            total_amount=0.0,
            created_at="2026-09-29T10:20:00",
            lines=[
                SaleLine(
                    product_id=product.id,
                    quantity=2,
                    unit_price=500.0,
                ),
            ],
        )

        sale_service.create_sale(sale)

        assert sale.id is not None
        assert sale.total_amount == 1000.0

        persisted_product = product_repository.get_by_id(product.id)

        assert persisted_product is not None
        assert persisted_product.quantity == 8

        invoice = sale_invoice_service.create_invoice_for_sale(sale.id)

        assert invoice.id is not None
        assert invoice.sale_id == sale.id
        assert invoice.invoice_number == "INV-000001"
        assert invoice.total_amount == 1000.0

        stored_invoice = invoice_repository.get_by_id(invoice.id)

        assert stored_invoice is not None
        assert stored_invoice.sale_id == sale.id
        assert stored_invoice.total_amount == 1000.0

        assert reporting_service.get_sales_total() == 1000.0

        assert reporting_service.get_sales_by_date() == [
            {
                "sale_date": "2026-09-29",
                "sale_count": 1,
                "total_amount": 1000.0,
            }
        ]

        assert reporting_service.get_sales_by_product() == [
            {
                "product_id": product.id,
                "product_name": "End-to-End Product",
                "quantity_sold": 2,
                "sales_amount": 1000.0,
            }
        ]

    finally:
        connection.close()
