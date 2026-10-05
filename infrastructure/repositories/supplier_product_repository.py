from sqlite3 import Connection

from infrastructure.database.transaction import commit_if_needed


class SupplierProductRepository:
    """Persistence for the many-to-many Supplier ↔ Product relationship."""

    def __init__(self, connection: Connection) -> None:
        self.connection = connection

    def add(self, supplier_id: int, product_id: int) -> None:
        self.connection.execute(
            """
            INSERT OR IGNORE INTO supplier_products (supplier_id, product_id)
            VALUES (?, ?)
            """,
            (supplier_id, product_id),
        )
        commit_if_needed(self.connection)

    def remove(self, supplier_id: int, product_id: int) -> None:
        self.connection.execute(
            """
            DELETE FROM supplier_products
            WHERE supplier_id = ? AND product_id = ?
            """,
            (supplier_id, product_id),
        )
        commit_if_needed(self.connection)

    def get_product_ids_for_supplier(self, supplier_id: int) -> list[int]:
        rows = self.connection.execute(
            """
            SELECT product_id
            FROM supplier_products
            WHERE supplier_id = ?
            ORDER BY product_id
            """,
            (supplier_id,),
        ).fetchall()
        return [row[0] for row in rows]

    def get_supplier_ids_for_product(self, product_id: int) -> list[int]:
        rows = self.connection.execute(
            """
            SELECT supplier_id
            FROM supplier_products
            WHERE product_id = ?
            ORDER BY supplier_id
            """,
            (product_id,),
        ).fetchall()
        return [row[0] for row in rows]

    def exists(self, supplier_id: int, product_id: int) -> bool:
        row = self.connection.execute(
            """
            SELECT 1
            FROM supplier_products
            WHERE supplier_id = ? AND product_id = ?
            """,
            (supplier_id, product_id),
        ).fetchone()
        return row is not None
