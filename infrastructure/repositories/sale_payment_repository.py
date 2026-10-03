from sqlite3 import Connection

from domain.entities.sale_payment import SalePayment
from infrastructure.database.transaction import commit_if_needed
from infrastructure.repositories.base import Repository


class SalePaymentRepository(Repository[SalePayment]):
    """SQLite repository for SalePayment persistence."""

    def __init__(self, connection: Connection) -> None:
        self.connection = connection

    def add(self, entity: SalePayment) -> None:
        cursor = self.connection.execute(
            """
            INSERT INTO sale_payments (
                sale_id,
                payment_mode,
                amount,
                created_at
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                entity.sale_id,
                entity.payment_mode,
                entity.amount,
                entity.created_at,
            ),
        )

        entity.id = cursor.lastrowid
        commit_if_needed(self.connection)

    def get_by_id(self, entity_id: int) -> SalePayment | None:
        row = self.connection.execute(
            """
            SELECT
                id,
                sale_id,
                payment_mode,
                amount,
                created_at
            FROM sale_payments
            WHERE id = ?
            """,
            (entity_id,),
        ).fetchone()

        if row is None:
            return None

        return SalePayment(
            id=row[0],
            sale_id=row[1],
            payment_mode=row[2],
            amount=row[3],
            created_at=row[4],
        )

    def get_by_sale_id(self, sale_id: int) -> list[SalePayment]:
        rows = self.connection.execute(
            """
            SELECT
                id,
                sale_id,
                payment_mode,
                amount,
                created_at
            FROM sale_payments
            WHERE sale_id = ?
            ORDER BY id
            """,
            (sale_id,),
        ).fetchall()

        return [
            SalePayment(
                id=row[0],
                sale_id=row[1],
                payment_mode=row[2],
                amount=row[3],
                created_at=row[4],
            )
            for row in rows
        ]

    def get_all(self) -> list[SalePayment]:
        rows = self.connection.execute(
            """
            SELECT
                id,
                sale_id,
                payment_mode,
                amount,
                created_at
            FROM sale_payments
            ORDER BY id
            """
        ).fetchall()

        return [
            SalePayment(
                id=row[0],
                sale_id=row[1],
                payment_mode=row[2],
                amount=row[3],
                created_at=row[4],
            )
            for row in rows
        ]

    def delete(self, entity_id: int) -> None:
        self.connection.execute(
            """
            DELETE FROM sale_payments
            WHERE id = ?
            """,
            (entity_id,),
        )
        commit_if_needed(self.connection)