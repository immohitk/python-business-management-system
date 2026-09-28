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


def seed_customer_supplier_data(connection) -> None:
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
                "2026-09-28T10:00:00",
            ),
            (
                "Customer B",
                "2222222222",
                "b@example.com",
                "Address B",
                "2026-09-28T10:05:00",
            ),
        ],
    )

    connection.executemany(
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
        [
            (
                "Supplier A",
                "3333333333",
                "supplier-a@example.com",
                "Supplier Address A",
                "2026-09-28T10:10:00",
            ),
            (
                "Supplier B",
                "4444444444",
                "supplier-b@example.com",
                "Supplier Address B",
                "2026-09-28T10:15:00",
            ),
        ],
    )

    connection.commit()


def test_customer_and_supplier_reporting_works_through_real_database(
    tmp_path,
):
    service, connection = create_service(tmp_path)

    try:
        seed_customer_supplier_data(connection)

        assert service.get_customers_summary() == [
            {
                "customer_id": 1,
                "customer_name": "Customer A",
                "phone": "1111111111",
                "email": "a@example.com",
            },
            {
                "customer_id": 2,
                "customer_name": "Customer B",
                "phone": "2222222222",
                "email": "b@example.com",
            },
        ]

        assert service.get_suppliers_summary() == [
            {
                "supplier_id": 1,
                "supplier_name": "Supplier A",
                "phone": "3333333333",
                "email": "supplier-a@example.com",
            },
            {
                "supplier_id": 2,
                "supplier_name": "Supplier B",
                "phone": "4444444444",
                "email": "supplier-b@example.com",
            },
        ]
    finally:
        connection.close()
