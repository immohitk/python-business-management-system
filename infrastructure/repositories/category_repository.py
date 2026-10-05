from sqlite3 import Connection

from domain.entities.category import Category
from infrastructure.database.transaction import commit_if_needed
from infrastructure.repositories.base import Repository


class CategoryRepository(Repository[Category]):
    def __init__(self, connection: Connection):
        self.connection = connection

    def add(self, entity: Category) -> None:
        cursor = self.connection.execute(
            "INSERT INTO categories (name, description) VALUES (?, ?)",
            (entity.name, entity.description),
        )
        entity.id = cursor.lastrowid
        commit_if_needed(self.connection)

    def get_by_id(self, entity_id: int):
        row = self.connection.execute(
            "SELECT id, name, description FROM categories WHERE id=?",
            (entity_id,),
        ).fetchone()
        return None if row is None else Category(row[0], row[1], row[2])

    def get_all(self):
        rows = self.connection.execute(
            "SELECT id, name, description FROM categories ORDER BY id"
        ).fetchall()
        return [Category(row[0], row[1], row[2]) for row in rows]

    def update(self, entity: Category) -> None:
        self.connection.execute(
            "UPDATE categories SET name=?, description=? WHERE id=?",
            (entity.name, entity.description, entity.id),
        )
        commit_if_needed(self.connection)

    def delete(self, entity_id: int) -> None:
        self.connection.execute("DELETE FROM categories WHERE id=?", (entity_id,))
        commit_if_needed(self.connection)
