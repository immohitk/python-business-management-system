from sqlite3 import Connection

from domain.entities.invoice import Invoice
from infrastructure.repositories.base import Repository


class InvoiceRepository(Repository[Invoice]):
    """SQLite repository for Invoice persistence."""

    def __init__(self, connection: Connection) -> None:
        self.connection = connection

    def add(self, entity: Invoice) -> None:
        cursor = self.connection.execute(
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
                entity.sale_id,
                entity.invoice_number,
                entity.invoice_date,
                entity.total_amount,
                entity.created_at,
            ),
        )

        entity.id = cursor.lastrowid
        self.connection.commit()

    def get_by_id(self, entity_id: int) -> Invoice | None:
        row = self.connection.execute(
            """
            SELECT
                id,
                sale_id,
                invoice_number,
                invoice_date,
                total_amount,
                created_at
            FROM invoices
            WHERE id = ?
            """,
            (entity_id,),
        ).fetchone()

        if row is None:
            return None

        return Invoice(
            id=row[0],
            sale_id=row[1],
            invoice_number=row[2],
            invoice_date=row[3],
            total_amount=row[4],
            created_at=row[5],
        )

    def get_all(self) -> list[Invoice]:
        rows = self.connection.execute(
            """
            SELECT
                id,
                sale_id,
                invoice_number,
                invoice_date,
                total_amount,
                created_at
            FROM invoices
            ORDER BY id
            """
        ).fetchall()

        return [
            Invoice(
                id=row[0],
                sale_id=row[1],
                invoice_number=row[2],
                invoice_date=row[3],
                total_amount=row[4],
                created_at=row[5],
            )
            for row in rows
        ]

    def delete(self, entity_id: int) -> None:
        self.connection.execute(
            """
            DELETE FROM invoices
            WHERE id = ?
            """,
            (entity_id,),
        )
        self.connection.commit()