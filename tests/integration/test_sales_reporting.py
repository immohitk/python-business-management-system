from pathlib import Path

from application.services.reporting_service import ReportingService
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
