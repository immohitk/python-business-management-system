from sqlite3 import Connection

from domain.entities.stock_movement import StockMovement, StockMovementType
from infrastructure.repositories.base import Repository
from infrastructure.database.transaction import commit_if_needed


class StockMovementRepository(Repository[StockMovement]):
    """SQLite repository for StockMovement persistence."""

    def __init__(self, connection: Connection) -> None:
        self.connection = connection

    def add(self, entity: StockMovement) -> None:
        raise NotImplementedError

    def get_by_id(self, entity_id: int) -> StockMovement | None:
        row = self.connection.execute(
            """
            SELECT
                movement_type,
                quantity,
                resulting_stock,
                created_at
            FROM stock_movements
            WHERE id = ?
            """,
            (entity_id,),
        ).fetchone()

        if row is None:
            return None

        return StockMovement(
            movement_type=StockMovementType(row[0]),
            quantity=row[1],
            resulting_stock=row[2],
            created_at=row[3],
        )

    def get_all(self) -> list[StockMovement]:
        rows = self.connection.execute(
            """
            SELECT
                movement_type,
                quantity,
                resulting_stock,
                created_at
            FROM stock_movements
            ORDER BY id
            """
        ).fetchall()

        return [
            StockMovement(
                movement_type=StockMovementType(row[0]),
                quantity=row[1],
                resulting_stock=row[2],
                created_at=row[3],
            )
            for row in rows
        ]

    def delete(self, entity_id: int) -> None:
        self.connection.execute(
            """
            DELETE FROM stock_movements
            WHERE id = ?
            """,
            (entity_id,),
        )
        commit_if_needed(self.connection)

    def add_movement(
        self,
        product_id: int,
        entity: StockMovement,
    ) -> None:
        self.connection.execute(
            """
            INSERT INTO stock_movements (
                product_id,
                movement_type,
                quantity,
                resulting_stock,
                created_at
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                product_id,
                entity.movement_type.value,
                entity.quantity,
                entity.resulting_stock,
                entity.created_at,
            ),
        )
        commit_if_needed(self.connection)

    def get_movements(self, product_id: int) -> list[StockMovement]:
        rows = self.connection.execute(
            """
            SELECT
                movement_type,
                quantity,
                resulting_stock,
                created_at
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
                created_at=row[3],
            )
            for row in rows
        ]
