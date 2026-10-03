from sqlite3 import Connection

from domain.entities.tax_charge import TaxCharge
from infrastructure.repositories.base import Repository
from infrastructure.database.transaction import commit_if_needed


class TaxChargeRepository(Repository[TaxCharge]):
    """SQLite repository for TaxCharge persistence."""

    def __init__(self, connection: Connection) -> None:
        self.connection = connection

    def add(self, entity: TaxCharge) -> None:
        cursor = self.connection.execute(
            """
            INSERT INTO taxes_charges (
                name,
                type,
                calculation,
                value,
                scope,
                product_id,
                is_active,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                entity.name,
                entity.type,
                entity.calculation,
                entity.value,
                entity.scope,
                entity.product_id,
                int(entity.is_active),
                entity.created_at,
            ),
        )

        entity.id = cursor.lastrowid
        commit_if_needed(self.connection)

    def update(self, entity: TaxCharge) -> None:
        self.connection.execute(
            """
            UPDATE taxes_charges
            SET
                name=?,
                type=?,
                calculation=?,
                value=?,
                scope=?,
                product_id=?,
                is_active=?,
                created_at=?
            WHERE id=?
            """,
            (
                entity.name,
                entity.type,
                entity.calculation,
                entity.value,
                entity.scope,
                entity.product_id,
                int(entity.is_active),
                entity.created_at,
                entity.id,
            ),
        )

        commit_if_needed(self.connection)

    def get_by_id(self, entity_id: int) -> TaxCharge | None:
        row = self.connection.execute(
            """
            SELECT
                id,
                name,
                type,
                calculation,
                value,
                scope,
                product_id,
                is_active,
                created_at
            FROM taxes_charges
            WHERE id = ?
            """,
            (entity_id,),
        ).fetchone()

        if row is None:
            return None

        return TaxCharge(
            id=row[0],
            name=row[1],
            type=row[2],
            calculation=row[3],
            value=row[4],
            scope=row[5],
            product_id=row[6],
            is_active=bool(row[7]),
            created_at=row[8],
        )

    def get_all(self) -> list[TaxCharge]:
        rows = self.connection.execute(
            """
            SELECT
                id,
                name,
                type,
                calculation,
                value,
                scope,
                product_id,
                is_active,
                created_at
            FROM taxes_charges
            ORDER BY id
            """
        ).fetchall()

        return [
            TaxCharge(
                id=row[0],
                name=row[1],
                type=row[2],
                calculation=row[3],
                value=row[4],
                scope=row[5],
                product_id=row[6],
                is_active=bool(row[7]),
                created_at=row[8],
            )
            for row in rows
        ]

    def delete(self, entity_id: int) -> None:
        self.connection.execute(
            """
            DELETE FROM taxes_charges
            WHERE id = ?
            """,
            (entity_id,),
        )

        commit_if_needed(self.connection)