from pathlib import Path

from domain.entities.category import Category
from infrastructure.database.connection import get_connection
from infrastructure.database.initialization import initialize_database
from infrastructure.repositories.category_repository import CategoryRepository


def test_category_crud(tmp_path: Path):
    database_path = tmp_path / "test.db"
    initialize_database(database_path)
    connection = get_connection(database_path)
    repository = CategoryRepository(connection)

    try:
        category = Category(id=None, name="Groceries", description="Food")
        repository.add(category)

        assert category.id is not None
        assert repository.get_by_id(category.id) == category

        category.description = "Food and household items"
        repository.update(category)
        assert repository.get_by_id(category.id) == category

        assert repository.get_all() == [category]

        repository.delete(category.id)
        assert repository.get_by_id(category.id) is None
    finally:
        connection.close()
