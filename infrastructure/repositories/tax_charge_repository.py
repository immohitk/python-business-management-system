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
                created_at,
                tax_code,
                is_default
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
                entity.tax_code,
                int(entity.is_default),
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
                created_at=?,
                tax_code=?,
                is_default=?
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
                entity.tax_code,
                int(entity.is_default),
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
                created_at,
                tax_code,
                is_default
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
            tax_code=row[9],
            is_default=bool(row[10]),
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
                created_at,
                tax_code,
                is_default
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
                tax_code=row[9],
                is_default=bool(row[10]),
            )
            for row in rows
        ]

    def get_defaults(self) -> list[TaxCharge]:
        return [tax_charge for tax_charge in self.get_all() if tax_charge.is_active and tax_charge.is_default]

    def snapshot_for_sale(self, sale_id: int, tax_charge: TaxCharge, amount: float, created_at: str) -> None:
        self.connection.execute(
            """
            INSERT INTO sale_tax_charge_snapshots (
                sale_id, tax_charge_id, name, type, calculation, value,
                scope, product_id, amount, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                sale_id, tax_charge.id, tax_charge.name, tax_charge.type,
                tax_charge.calculation, tax_charge.value, tax_charge.scope,
                tax_charge.product_id, amount, created_at,
            ),
        )

    def get_sale_snapshots(self, sale_id: int) -> list[dict]:
        rows = self.connection.execute(
            """
            SELECT id, sale_id, tax_charge_id, name, type, calculation, value,
                   scope, product_id, amount, created_at
            FROM sale_tax_charge_snapshots
            WHERE sale_id = ?
            ORDER BY id
            """,
            (sale_id,),
        ).fetchall()
        return [
            {
                "id": row[0], "sale_id": row[1], "tax_charge_id": row[2],
                "name": row[3], "type": row[4], "calculation": row[5],
                "value": row[6], "scope": row[7], "product_id": row[8],
                "amount": row[9], "created_at": row[10],
            }
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