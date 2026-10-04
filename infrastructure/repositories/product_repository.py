from datetime import datetime
from sqlite3 import Connection

from domain.entities.product import Product
from domain.entities.stock_movement import StockMovement, StockMovementType
from infrastructure.repositories.base import Repository
from infrastructure.database.transaction import commit_if_needed


class ProductRepository(Repository[Product]):
    def __init__(self, connection: Connection):
        self.connection = connection

    def add(self, entity: Product) -> None:
        cursor = self.connection.execute(
            """
            INSERT INTO products (
                name, description, sku, price, quantity, created_at
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

        self.connection.execute(
            """
            INSERT INTO product_history (
                product_id,
                action,
                product_name,
                product_code,
                details,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                entity.id,
                "ADD",
                entity.name,
                entity.sku,
                "Product added",
                entity.created_at,
            ),
        )

        commit_if_needed(self.connection)

    def update(self, entity: Product) -> None:
        existing = self.get_by_id(entity.id)

        if existing is None:
            return

        changed_fields = []

        if existing.name != entity.name:
            changed_fields.append("Name")

        if existing.description != entity.description:
            changed_fields.append("Description")

        if existing.sku != entity.sku:
            changed_fields.append("Product Code")

        if existing.price != entity.price:
            changed_fields.append("Per Unit Price")

        self.connection.execute(
            """
            UPDATE products
            SET name=?, description=?, sku=?, price=?, quantity=?, created_at=?
            WHERE id=?
            """,
            (
                entity.name,
                entity.description,
                entity.sku,
                entity.price,
                entity.quantity,
                entity.created_at,
                entity.id,
            ),
        )

        details = (
            "Updated: " + ", ".join(changed_fields)
            if changed_fields
            else "Product updated"
        )

        self.connection.execute(
            """
            INSERT INTO product_history (
                product_id,
                action,
                product_name,
                product_code,
                details,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                entity.id,
                "EDIT",
                entity.name,
                entity.sku,
                details,
                datetime.now().isoformat(timespec="seconds"),
            ),
        )

        commit_if_needed(self.connection)

    def get_by_id(self, entity_id: int):
        cursor = self.connection.execute(
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
            WHERE id=?
            """,
            (entity_id,),
        )

        row = cursor.fetchone()

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

    def get_all(self):
        cursor = self.connection.execute(
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
        )

        products = []

        for row in cursor.fetchall():
            products.append(
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
            )

        return products

    def delete(self, entity_id: int) -> None:
        existing = self.get_by_id(entity_id)

        if existing is None:
            return

        self.connection.execute(
            """
            INSERT INTO product_history (
                product_id,
                action,
                product_name,
                product_code,
                details,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                existing.id,
                "DELETE",
                existing.name,
                existing.sku,
                "Product deleted",
                datetime.now().isoformat(timespec="seconds"),
            ),
        )

        self.connection.execute(
            """
            DELETE FROM products
            WHERE id=?
            """,
            (entity_id,),
        )

        commit_if_needed(self.connection)

    def get_edit_history(self, product_id: int):
        cursor = self.connection.execute(
            """
            SELECT
                id,
                product_id,
                action,
                product_name,
                product_code,
                details,
                created_at
            FROM product_history
            WHERE product_id=?
              AND action='EDIT'
            ORDER BY id DESC
            """,
            (product_id,),
        )

        return cursor.fetchall()

    def get_product_history(self):
        cursor = self.connection.execute(
            """
            SELECT
                id,
                product_id,
                action,
                product_name,
                product_code,
                details,
                created_at
            FROM product_history
            WHERE action IN ('ADD', 'DELETE')
            ORDER BY id DESC
            """
        )

        return cursor.fetchall()

    def _get_movements(self, product_id: int):
        cursor = self.connection.execute(
            """
            SELECT
                movement_type,
                quantity,
                resulting_stock,
                created_at
            FROM stock_movements
            WHERE product_id=?
            ORDER BY id
            """,
            (product_id,),
        )

        movements = []

        for row in cursor.fetchall():
            movements.append(
                StockMovement(
                    movement_type=StockMovementType(row[0]),
                    quantity=row[1],
                    resulting_stock=row[2],
                    created_at=row[3],
                )
            )

        return movements
