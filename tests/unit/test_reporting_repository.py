from pathlib import Path

from infrastructure.database.connection import get_connection
from infrastructure.database.initialization import initialize_database
from infrastructure.repositories.reporting_repository import ReportingRepository


def create_repository(tmp_path: Path) -> tuple[ReportingRepository, object]:
    database_path = tmp_path / "test.db"
    initialize_database(database_path)
    connection = get_connection(database_path)

    return ReportingRepository(connection), connection


def test_get_business_summary_returns_zero_counts_for_empty_database(tmp_path):
    repository, connection = create_repository(tmp_path)

    try:
        summary = repository.get_business_summary()

        assert summary == {
            "product_count": 0,
            "customer_count": 0,
            "supplier_count": 0,
            "sale_count": 0,
            "invoice_count": 0,
        }
    finally:
        connection.close()


def test_get_business_summary_returns_controlled_counts(tmp_path):
    repository, connection = create_repository(tmp_path)

    try:
        connection.executemany(
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
            [
                (
                    "Product A",
                    "First product",
                    "SKU-A",
                    100.0,
                    10,
                    "2026-09-28T10:00:00",
                ),
                (
                    "Product B",
                    "Second product",
                    "SKU-B",
                    200.0,
                    20,
                    "2026-09-28T10:05:00",
                ),
            ],
        )

        connection.executemany(
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
            [
                (
                    "Customer A",
                    "1111111111",
                    "a@example.com",
                    "Address A",
                    "2026-09-28T10:10:00",
                ),
                (
                    "Customer B",
                    "2222222222",
                    "b@example.com",
                    "Address B",
                    "2026-09-28T10:15:00",
                ),
                (
                    "Customer C",
                    "3333333333",
                    "c@example.com",
                    "Address C",
                    "2026-09-28T10:20:00",
                ),
            ],
        )

        connection.execute(
            """
            INSERT INTO suppliers (
                name,
                phone,
                email,
                address,
                created_at
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                "Supplier A",
                "4444444444",
                "supplier@example.com",
                "Supplier Address",
                "2026-09-28T10:25:00",
            ),
        )

        connection.executemany(
            """
            INSERT INTO sales (
                customer_id,
                sale_date,
                total_amount,
                created_at
            )
            VALUES (?, ?, ?, ?)
            """,
            [
                (1, "2026-09-28", 1000.0, "2026-09-28T10:30:00"),
                (2, "2026-09-28", 2000.0, "2026-09-28T10:35:00"),
            ],
        )

        connection.executemany(
            """
            INSERT INTO invoices (
                sale_id,
                invoice_number,
                invoice_date,
                total_amount,
                created_at
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            [
                (
                    1,
                    "INV-001",
                    "2026-09-28",
                    1000.0,
                    "2026-09-28T10:40:00",
                ),
                (
                    2,
                    "INV-002",
                    "2026-09-28",
                    2000.0,
                    "2026-09-28T10:45:00",
                ),
            ],
        )

        connection.commit()

        summary = repository.get_business_summary()

        assert summary == {
            "product_count": 2,
            "customer_count": 3,
            "supplier_count": 1,
            "sale_count": 2,
            "invoice_count": 2,
        }
    finally:
        connection.close()
