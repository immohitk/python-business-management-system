from pathlib import Path

from infrastructure.database.connection import get_connection
from infrastructure.database.initialization import initialize_database
from infrastructure.repositories.reporting_repository import ReportingRepository


def create_repository(tmp_path: Path) -> tuple[ReportingRepository, object]:
    database_path = tmp_path / "test.db"
    initialize_database(database_path)
    connection = get_connection(database_path)

    return ReportingRepository(connection), connection


def seed_sales_data(connection) -> None:
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
                "Paint",
                "Interior paint",
                "PAINT-001",
                450.0,
                20,
                "2026-09-28T10:00:00",
            ),
            (
                "Brush",
                "Paint brush",
                "BRUSH-001",
                120.0,
                30,
                "2026-09-28T10:05:00",
            ),
        ],
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
            "2026-09-28T10:10:00",
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
            (1, "2026-09-27", 1020.0, "2026-09-27T10:00:00"),
            (1, "2026-09-27", 450.0, "2026-09-27T11:00:00"),
            (1, "2026-09-28", 240.0, "2026-09-28T10:00:00"),
        ],
    )

    connection.executemany(
        """
        INSERT INTO sale_items (
            sale_id,
            product_id,
            quantity,
            unit_price
        )
        VALUES (?, ?, ?, ?)
        """,
        [
            (1, 1, 2, 450.0),
            (1, 2, 1, 120.0),
            (2, 1, 1, 450.0),
            (3, 2, 2, 120.0),
        ],
    )

    connection.commit()


def test_get_sales_total_returns_total_amount(tmp_path):
    repository, connection = create_repository(tmp_path)

    try:
        seed_sales_data(connection)

        result = repository.get_sales_total()

        assert result == 1710.0
    finally:
        connection.close()


def test_get_sales_by_date_returns_expected_summaries(tmp_path):
    repository, connection = create_repository(tmp_path)

    try:
        seed_sales_data(connection)

        result = repository.get_sales_by_date()

        assert result == [
            {
                "sale_date": "2026-09-27",
                "sale_count": 2,
                "total_amount": 1470.0,
            },
            {
                "sale_date": "2026-09-28",
                "sale_count": 1,
                "total_amount": 240.0,
            },
        ]
    finally:
        connection.close()


def test_get_sales_by_product_returns_expected_summaries(tmp_path):
    repository, connection = create_repository(tmp_path)

    try:
        seed_sales_data(connection)

        result = repository.get_sales_by_product()

        assert result == [
            {
                "product_id": 1,
                "product_name": "Paint",
                "quantity_sold": 3,
                "sales_amount": 1350.0,
            },
            {
                "product_id": 2,
                "product_name": "Brush",
                "quantity_sold": 3,
                "sales_amount": 360.0,
            },
        ]
    finally:
        connection.close()
