from sqlite3 import Connection

from domain.entities.sale import Sale
from domain.entities.sale_item import SaleItem
from infrastructure.repositories.base import Repository


class SaleRepository(Repository[Sale]):
    """SQLite repository for Sale persistence."""

    def __init__(self, connection: Connection) -> None:
        self.connection = connection

    def add(self, entity: Sale) -> None:
        cursor = self.connection.execute(
            """
            INSERT INTO sales (
                customer_id,
                sale_date,
                total_amount,
                created_at
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                entity.customer_id,
                entity.sale_date,
                entity.total_amount,
                entity.created_at,
            ),
        )

        entity.id = cursor.lastrowid
        self.connection.commit()

    def get_by_id(self, entity_id: int) -> Sale | None:
        row = self.connection.execute(
            """
            SELECT
                id,
                customer_id,
                sale_date,
                total_amount,
                created_at
            FROM sales
            WHERE id = ?
            """,
            (entity_id,),
        ).fetchone()

        if row is None:
            return None

        return Sale(
            id=row[0],
            customer_id=row[1],
            sale_date=row[2],
            total_amount=row[3],
            created_at=row[4],
        )

    def get_all(self) -> list[Sale]:
        rows = self.connection.execute(
            """
            SELECT
                id,
                customer_id,
                sale_date,
                total_amount,
                created_at
            FROM sales
            ORDER BY id
            """
        ).fetchall()

        return [
            Sale(
                id=row[0],
                customer_id=row[1],
                sale_date=row[2],
                total_amount=row[3],
                created_at=row[4],
            )
            for row in rows
        ]

    def delete(self, entity_id: int) -> None:
        self.connection.execute(
            """
            DELETE FROM sales
            WHERE id = ?
            """,
            (entity_id,),
        )
        self.connection.commit()

    def add_item(self, entity: SaleItem) -> None:
        cursor = self.connection.execute(
            """
            INSERT INTO sale_items (
                sale_id,
                product_id,
                quantity,
                unit_price
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                entity.sale_id,
                entity.product_id,
                entity.quantity,
                entity.unit_price,
            ),
        )

        entity.id = cursor.lastrowid
        self.connection.commit()

    def get_items(self, sale_id: int) -> list[SaleItem]:
        rows = self.connection.execute(
            """
            SELECT
                id,
                sale_id,
                product_id,
                quantity,
                unit_price
            FROM sale_items
            WHERE sale_id = ?
            ORDER BY id
            """,
            (sale_id,),
        ).fetchall()

        return [
            SaleItem(
                id=row[0],
                sale_id=row[1],
                product_id=row[2],
                quantity=row[3],
                unit_price=row[4],
            )
            for row in rows
        ]