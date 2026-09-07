from sqlite3 import Connection

from domain.entities.customer import Customer
from infrastructure.repositories.base import Repository


class CustomerRepository(Repository[Customer]):
    """SQLite repository for Customer persistence."""

    def __init__(self, connection: Connection) -> None:
        self.connection = connection

    def add(self, entity: Customer) -> None:
        cursor = self.connection.execute(
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
                entity.name,
                entity.phone,
                entity.email,
                entity.address,
                entity.created_at,
            ),
        )

        entity.id = cursor.lastrowid
        self.connection.commit()

    def get_by_id(self, entity_id: int) -> Customer | None:
        row = self.connection.execute(
            """
            SELECT
                id,
                name,
                phone,
                email,
                address,
                created_at
            FROM customers
            WHERE id = ?
            """,
            (entity_id,),
        ).fetchone()

        if row is None:
            return None

        return Customer(
            id=row[0],
            name=row[1],
            phone=row[2],
            email=row[3],
            address=row[4],
            created_at=row[5],
        )

    def get_all(self) -> list[Customer]:
        rows = self.connection.execute(
            """
            SELECT
                id,
                name,
                phone,
                email,
                address,
                created_at
            FROM customers
            ORDER BY id
            """
        ).fetchall()

        return [
            Customer(
                id=row[0],
                name=row[1],
                phone=row[2],
                email=row[3],
                address=row[4],
                created_at=row[5],
            )
            for row in rows
        ]

    def delete(self, entity_id: int) -> None:
        self.connection.execute(
            """
            DELETE FROM customers
            WHERE id = ?
            """,
            (entity_id,),
        )
        self.connection.commit()