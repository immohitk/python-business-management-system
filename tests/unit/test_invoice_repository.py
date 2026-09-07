from pathlib import Path

from domain.entities.invoice import Invoice
from infrastructure.database.connection import get_connection
from infrastructure.database.initialization import initialize_database
from infrastructure.repositories.invoice_repository import InvoiceRepository
from infrastructure.repositories.sale_repository import SaleRepository


def create_repositories(
    tmp_path: Path,
) -> tuple[InvoiceRepository, SaleRepository, object]:
    database_path = tmp_path / "test.db"
    initialize_database(database_path)
    connection = get_connection(database_path)

    return (
        InvoiceRepository(connection),
        SaleRepository(connection),
        connection,
    )


def create_customer(connection) -> int:
    cursor = connection.execute(
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
            "Test Customer",
            "9876543210",
            "customer@example.com",
            "Delhi",
            "2026-09-07T20:00:00",
        ),
    )
    connection.commit()

    return cursor.lastrowid


def create_sale(connection) -> int:
    customer_id = create_customer(connection)

    sale_repository = SaleRepository(connection)

    from domain.entities.sale import Sale

    sale = Sale(
        id=None,
        customer_id=customer_id,
        sale_date="2026-09-07",
        total_amount=900.0,
        created_at="2026-09-07T20:00:00",
    )

    sale_repository.add(sale)

    return sale.id


def create_invoice(connection) -> Invoice:
    sale_id = create_sale(connection)

    return Invoice(
        id=None,
        sale_id=sale_id,
        invoice_number="INV-001",
        invoice_date="2026-09-07",
        total_amount=900.0,
        created_at="2026-09-07T20:00:00",
    )


def test_add_invoice(tmp_path):
    repository, _, connection = create_repositories(tmp_path)

    try:
        invoice = create_invoice(connection)

        repository.add(invoice)

        assert invoice.id is not None
        assert invoice.id > 0
    finally:
        connection.close()


def test_get_invoice_by_id(tmp_path):
    repository, _, connection = create_repositories(tmp_path)

    try:
        invoice = create_invoice(connection)
        repository.add(invoice)

        result = repository.get_by_id(invoice.id)

        assert result == invoice
    finally:
        connection.close()


def test_get_invoice_by_id_returns_none_for_missing_invoice(tmp_path):
    repository, _, connection = create_repositories(tmp_path)

    try:
        result = repository.get_by_id(999)

        assert result is None
    finally:
        connection.close()


def test_get_all_invoices(tmp_path):
    repository, _, connection = create_repositories(tmp_path)

    try:
        first_invoice = create_invoice(connection)
        second_invoice = create_invoice(connection)
        second_invoice.invoice_number = "INV-002"

        repository.add(first_invoice)
        repository.add(second_invoice)

        result = repository.get_all()

        assert result == [first_invoice, second_invoice]
    finally:
        connection.close()


def test_delete_invoice(tmp_path):
    repository, _, connection = create_repositories(tmp_path)

    try:
        invoice = create_invoice(connection)
        repository.add(invoice)

        repository.delete(invoice.id)

        assert repository.get_by_id(invoice.id) is None
    finally:
        connection.close()