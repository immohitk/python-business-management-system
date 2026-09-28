from pathlib import Path

from infrastructure.database.connection import get_connection
from infrastructure.database.initialization import initialize_database
from infrastructure.repositories.reporting_repository import ReportingRepository


def create_repository(tmp_path: Path) -> tuple[ReportingRepository, object]:
    database_path = tmp_path / "test.db"
    initialize_database(database_path)
    connection = get_connection(database_path)

    return ReportingRepository(connection), connection


def seed_inventory_data(connection) -> None:
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
                2,
                "2026-09-28T10:00:00",
            ),
            (
                "Brush",
                "Paint brush",
                "BRUSH-001",
                15,
                20,
                "2026-09-28T10:05:00",
            ),
            (
                "Roller",
                "Paint roller",
                "ROLLER-001",
                250.0,
                5,
                "2026-09-28T10:10:00",
            ),
        ],
    )

    connection.executemany(
        """
        INSERT INTO stock_movements (
            product_id,
            movement_type,
            quantity,
            resulting_stock,
            created_at
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        [
            (1, "ADD", 10, 10, "2026-09-28T11:00:00"),
            (1, "DEDUCT", 8, 2, "2026-09-28T11:30:00"),
            (2, "ADD", 25, 25, "2026-09-28T12:00:00"),
            (2, "ADJUST", 5, 20, "2026-09-28T12:30:00"),
            (3, "ADD", 5, 5, "2026-09-28T13:00:00"),
        ],
    )

    connection.commit()


def test_get_stock_status_returns_current_product_stock(tmp_path):
    repository, connection = create_repository(tmp_path)

    try:
        seed_inventory_data(connection)

        result = repository.get_stock_status()

        assert result == [
            {
                "product_id": 1,
                "product_name": "Paint",
                "sku": "PAINT-001",
                "quantity": 2,
            },
            {
                "product_id": 2,
                "product_name": "Brush",
                "sku": "BRUSH-001",
                "quantity": 20,
            },
            {
                "product_id": 3,
                "product_name": "Roller",
                "sku": "ROLLER-001",
                "quantity": 5,
            },
        ]
    finally:
        connection.close()


def test_get_stock_movements_summary_returns_expected_totals(tmp_path):
    repository, connection = create_repository(tmp_path)

    try:
        seed_inventory_data(connection)

        result = repository.get_stock_movements_summary()

        assert result == [
            {
                "movement_type": "ADD",
                "movement_count": 3,
                "total_quantity": 40,
            },
            {
                "movement_type": "ADJUST",
                "movement_count": 1,
                "total_quantity": 5,
            },
            {
                "movement_type": "DEDUCT",
                "movement_count": 1,
                "total_quantity": 8,
            },
        ]
    finally:
        connection.close()


def test_get_low_stock_products_returns_products_at_or_below_threshold(
    tmp_path,
):
    repository, connection = create_repository(tmp_path)

    try:
        seed_inventory_data(connection)

        result = repository.get_low_stock_products(5)

        assert result == [
            {
                "product_id": 1,
                "product_name": "Paint",
                "sku": "PAINT-001",
                "quantity": 2,
            },
            {
                "product_id": 3,
                "product_name": "Roller",
                "sku": "ROLLER-001",
                "quantity": 5,
            },
        ]
    finally:
        connection.close()
