from sqlite3 import Connection

from domain.entities.unit import Unit
from infrastructure.database.transaction import commit_if_needed
from infrastructure.repositories.base import Repository


class UnitRepository(Repository[Unit]):
    def __init__(self, connection: Connection):
        self.connection = connection

    def add(self, entity: Unit) -> None:
        cursor = self.connection.execute(
            """
            INSERT INTO units (code, name, dimension, to_base_factor)
            VALUES (?, ?, ?, ?)
            """,
            (entity.code.upper(), entity.name, entity.dimension.upper(), entity.to_base_factor),
        )
        entity.id = cursor.lastrowid
        commit_if_needed(self.connection)

    def get_by_id(self, entity_id: int):
        row = self.connection.execute(
            "SELECT id, code, name, dimension, to_base_factor FROM units WHERE id=?",
            (entity_id,),
        ).fetchone()
        return None if row is None else Unit(row[1], row[2], row[3], row[4], row[0])

    def get_by_code(self, code: str):
        row = self.connection.execute(
            "SELECT id, code, name, dimension, to_base_factor FROM units WHERE code=?",
            (code.upper(),),
        ).fetchone()
        return None if row is None else Unit(row[1], row[2], row[3], row[4], row[0])

    def get_all(self):
        rows = self.connection.execute(
            "SELECT id, code, name, dimension, to_base_factor FROM units ORDER BY id"
        ).fetchall()
        return [Unit(row[1], row[2], row[3], row[4], row[0]) for row in rows]

    def update(self, entity: Unit) -> None:
        self.connection.execute(
            """
            UPDATE units
            SET code=?, name=?, dimension=?, to_base_factor=?
            WHERE id=?
            """,
            (entity.code.upper(), entity.name, entity.dimension.upper(), entity.to_base_factor, entity.id),
        )
        commit_if_needed(self.connection)

    def delete(self, entity_id: int) -> None:
        self.connection.execute("DELETE FROM units WHERE id=?", (entity_id,))
        commit_if_needed(self.connection)
