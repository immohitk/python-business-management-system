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


def test_inventory_reporting_works_through_real_database(tmp_path):
    service, connection = create_service(tmp_path)

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
                    120.0,
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

        assert service.get_stock_status() == [
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

        assert service.get_stock_movements_summary() == [
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

        assert service.get_low_stock_products(5) == [
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
