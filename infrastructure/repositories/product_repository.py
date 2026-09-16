from sqlite3 import Connection

from domain.entities.product import Product
from domain.entities.stock_movement import StockMovement, StockMovementType
from infrastructure.repositories.base import Repository


class ProductRepository(Repository[Product]):
    """SQLite repository for Product persistence."""

    def __init__(self, connection: Connection) -> None:
        self.connection = connection

    def add(self, entity: Product) -> None:
        cursor = self.connection.execute(
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
            (
                entity.name,
                entity.description,
                entity.sku,
                entity.price,
                entity.quantity,
                entity.created_at,
            ),
        )

        entity.id = cursor.lastrowid
        self.connection.commit()

    def get_by_id(self, entity_id: int) -> Product | None:
        row = self.connection.execute(
            """
            SELECT
                id,
                name,
                description,
                sku,
                price,
                quantity,
                created_at
            FROM products
            WHERE id = ?
            """,
            (entity_id,),
        ).fetchone()

        if row is None:
            return None

        return Product(
            id=row[0],
            name=row[1],
            description=row[2],
            sku=row[3],
            price=row[4],
            quantity=row[5],
            created_at=row[6],
            movements=self._get_movements(row[0]),
        )

    def get_all(self) -> list[Product]:
        rows = self.connection.execute(
            """
            SELECT
                id,
                name,
                description,
                sku,
                price,
                quantity,
                created_at
            FROM products
            ORDER BY id
            """
        ).fetchall()

        return [
            Product(
                id=row[0],
                name=row[1],
                description=row[2],
                sku=row[3],
                price=row[4],
                quantity=row[5],
                created_at=row[6],
                movements=self._get_movements(row[0]),
            )
            for row in rows
        ]

    def delete(self, entity_id: int) -> None:
        self.connection.execute(
            """
            DELETE FROM products
            WHERE id = ?
            """,
            (entity_id,),
        )
        self.connection.commit()

    def _get_movements(self, product_id: int) -> list[StockMovement]:
        rows = self.connection.execute(
            """
            SELECT
                movement_type,
                quantity,
                resulting_stock
            FROM stock_movements
            WHERE product_id = ?
            ORDER BY id
            """,
            (product_id,),
        ).fetchall()

        return [
            StockMovement(
                movement_type=StockMovementType(row[0]),
                quantity=row[1],
                resulting_stock=row[2],
            )
            for row in rows
        ]
