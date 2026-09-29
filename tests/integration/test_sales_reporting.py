from pathlib import Path

from domain.entities.customer import Customer
from domain.entities.product import Product
from domain.entities.sale import Sale
from domain.entities.sale_line import SaleLine
from application.services.reporting_service import ReportingService
from application.services.customer_service import CustomerService
from application.services.inventory_service import InventoryService
from application.services.product_service import ProductService
from application.services.sale_service import SaleService
from infrastructure.repositories.customer_repository import CustomerRepository
from infrastructure.repositories.product_repository import ProductRepository
from infrastructure.repositories.sale_repository import SaleRepository
from infrastructure.repositories.stock_movement_repository import (
    StockMovementRepository,
)
from infrastructure.database.connection import get_connection
from infrastructure.database.initialization import initialize_database
from infrastructure.repositories.reporting_repository import ReportingRepository


def create_service(tmp_path: Path) -> tuple[ReportingService, object]:
    database_path = tmp_path / "test.db"
    initialize_database(database_path)
    connection = get_connection(database_path)
    repository = ReportingRepository(connection)

    return ReportingService(repository), connection


def test_sales_reporting_works_through_real_database(tmp_path):
    service, connection = create_service(tmp_path)

    try:
        connection.execute(
            """
            INSERT INTO products (
                name,
                description,
                sku,
                price,
                quantity,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                "Paint",
                "Interior paint",
                "PAINT-001",
                450.0,
                20,
                "2026-09-28T10:00:00",
            ),
        )

        connection.execute(
            """
            INSERT INTO customers (
                name,
                phone,
                email,
                address,
                created_at
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                "Customer A",
                "1111111111",
                "a@example.com",
                "Address A",
                "2026-09-28T10:05:00",
            ),
        )

        connection.execute(
            """
            INSERT INTO sales (
                customer_id,
                sale_date,
                total_amount,
                created_at
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                1,
                "2026-09-28",
                900.0,
                "2026-09-28T10:10:00",
            ),
        )

        connection.execute(
            """
            INSERT INTO sale_items (
                sale_id,
                product_id,
                quantity,
                unit_price
            )
            VALUES (?, ?, ?, ?)
            """,
            (1, 1, 2, 450.0),
        )

        connection.commit()

        assert service.get_sales_total() == 900.0

        assert service.get_sales_by_date() == [
            {
                "sale_date": "2026-09-28",
                "sale_count": 1,
                "total_amount": 900.0,
            }
        ]

        assert service.get_sales_by_product() == [
            {
                "product_id": 1,
                "product_name": "Paint",
                "quantity_sold": 2,
                "sales_amount": 900.0,
            }
        ]
    finally:
        connection.close()


def test_sales_reporting_works_with_application_service_created_sale(
    tmp_path,
):
    database_path = tmp_path / "test.db"
    initialize_database(database_path)
    connection = get_connection(database_path)

    try:
        product_repository = ProductRepository(connection)
        customer_repository = CustomerRepository(connection)
        sale_repository = SaleRepository(connection)
        stock_movement_repository = StockMovementRepository(connection)
        reporting_repository = ReportingRepository(connection)

        product_service = ProductService(product_repository)
        customer_service = CustomerService(customer_repository)
        inventory_service = InventoryService(
            product_repository,
            stock_movement_repository,
        )
        sale_service = SaleService(
            sale_repository,
            inventory_service,
        )
        reporting_service = ReportingService(reporting_repository)

        product = Product(
            id=None,
            name="Reporting Product",
            description="Product created through application service",
            sku="REPORTING-001",
            price=450.0,
            quantity=0,
            created_at="2026-09-28T10:00:00",
        )

        customer = Customer(
            id=None,
            name="Reporting Customer",
            phone="1111111111",
            email="reporting@example.com",
            address="Bengaluru",
            created_at="2026-09-28T10:05:00",
        )

        product_service.add_product(product)
        customer_service.add_customer(customer)

        inventory_service.stock_in(
            product.id,
            10,
            created_at="2026-09-28T10:10:00",
        )

        sale = Sale(
            id=None,
            customer_id=customer.id,
            sale_date="2026-09-28",
            total_amount=0.0,
            created_at="2026-09-28T10:20:00",
            lines=[
                SaleLine(
                    product_id=product.id,
                    quantity=2,
                    unit_price=450.0,
                ),
            ],
        )

        sale_service.create_sale(sale)

        assert reporting_service.get_sales_total() == 900.0

        assert reporting_service.get_sales_by_date() == [
            {
                "sale_date": "2026-09-28",
                "sale_count": 1,
                "total_amount": 900.0,
            }
        ]

        assert reporting_service.get_sales_by_product() == [
            {
                "product_id": product.id,
                "product_name": "Reporting Product",
                "quantity_sold": 2,
                "sales_amount": 900.0,
            }
        ]

    finally:
        connection.close()
