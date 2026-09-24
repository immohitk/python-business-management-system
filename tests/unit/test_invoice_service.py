from pathlib import Path

from application.services.invoice_service import InvoiceService
from infrastructure.database.connection import get_connection
from infrastructure.database.initialization import initialize_database
from infrastructure.repositories.invoice_repository import InvoiceRepository


def create_service(tmp_path: Path) -> tuple[InvoiceService, object]:
    database_path = tmp_path / "test.db"
    initialize_database(database_path)
    connection = get_connection(database_path)

    invoice_repository = InvoiceRepository(connection)
    service = InvoiceService(invoice_repository)

    return service, connection


def test_generate_invoice_number_starts_at_one(tmp_path):
    service, connection = create_service(tmp_path)

    try:
        assert service.generate_invoice_number() == "INV-000001"
    finally:
        connection.close()


def test_generate_invoice_number_increments_existing_number(tmp_path):
    service, connection = create_service(tmp_path)

    try:
        connection.execute(
            """
            INSERT INTO customers (name, created_at)
            VALUES (?, ?)
            """,
            ("Test Customer", "2026-09-24T19:00:00"),
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
            (1, "2026-09-24", 100.0, "2026-09-24T19:00:00"),
        )

        connection.execute(
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
            (
                1,
                "INV-000007",
                "2026-09-24",
                100.0,
                "2026-09-24T19:00:00",
            ),
        )

        connection.commit()

        assert service.generate_invoice_number() == "INV-000008"
    finally:
        connection.close()


def test_generate_invoice_number_rejects_invalid_existing_format(tmp_path):
    service, connection = create_service(tmp_path)

    try:
        connection.execute(
            """
            INSERT INTO customers (name, created_at)
            VALUES (?, ?)
            """,
            ("Test Customer", "2026-09-24T19:00:00"),
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
            (1, "2026-09-24", 100.0, "2026-09-24T19:00:00"),
        )

        connection.execute(
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
            (
                1,
                "INVALID",
                "2026-09-24",
                100.0,
                "2026-09-24T19:00:00",
            ),
        )

        connection.commit()

        try:
            service.generate_invoice_number()
        except ValueError as exc:
            assert str(exc) == "Invalid invoice number format"
        else:
            raise AssertionError("Expected invalid invoice number to fail.")
    finally:
        connection.close()
