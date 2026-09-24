import sqlite3

import pytest
from pathlib import Path

from domain.entities.invoice import Invoice
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


def test_create_invoice_generates_and_persists_invoice_number(tmp_path):
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
            (1, "2026-09-24", 500.0, "2026-09-24T19:00:00"),
        )
        connection.commit()

        invoice = Invoice(
            id=None,
            sale_id=1,
            invoice_number="TEMP",
            invoice_date="2026-09-24",
            total_amount=500.0,
            created_at="2026-09-24T19:00:00",
        )

        result = service.create_invoice(invoice)

        assert result.id is not None
        assert result.invoice_number == "INV-000001"

        stored_invoice = InvoiceRepository(connection).get_by_id(result.id)

        assert stored_invoice is not None
        assert stored_invoice.invoice_number == "INV-000001"
    finally:
        connection.close()


def test_create_invoice_generates_sequential_numbers(tmp_path):
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
            (1, "2026-09-24", 500.0, "2026-09-24T19:00:00"),
        )
        connection.commit()

        first_invoice = Invoice(
            id=None,
            sale_id=1,
            invoice_number="TEMP",
            invoice_date="2026-09-24",
            total_amount=500.0,
            created_at="2026-09-24T19:00:00",
        )

        second_invoice = Invoice(
            id=None,
            sale_id=1,
            invoice_number="TEMP",
            invoice_date="2026-09-24",
            total_amount=750.0,
            created_at="2026-09-24T19:01:00",
        )

        service.create_invoice(first_invoice)
        service.create_invoice(second_invoice)

        assert first_invoice.invoice_number == "INV-000001"
        assert second_invoice.invoice_number == "INV-000002"
    finally:
        connection.close()


def test_invoice_numbers_must_be_unique(tmp_path):
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
            (1, "2026-09-24", 500.0, "2026-09-24T19:00:00"),
        )
        connection.commit()

        first_invoice = Invoice(
            id=None,
            sale_id=1,
            invoice_number="TEMP",
            invoice_date="2026-09-24",
            total_amount=500.0,
            created_at="2026-09-24T19:00:00",
        )

        service.create_invoice(first_invoice)

        duplicate_invoice = Invoice(
            id=None,
            sale_id=1,
            invoice_number="INV-000001",
            invoice_date="2026-09-24",
            total_amount=750.0,
            created_at="2026-09-24T19:01:00",
        )

        with pytest.raises(sqlite3.IntegrityError):
            service.invoice_repository.add(duplicate_invoice)
    finally:
        connection.close()
