from pathlib import Path

from infrastructure.database.connection import get_connection
from infrastructure.database.initialization import initialize_database
from infrastructure.repositories.unit_repository import UnitRepository


def test_standard_units_are_seeded(tmp_path: Path):
    database_path = tmp_path / "test.db"
    initialize_database(database_path)
    connection = get_connection(database_path)
    try:
        repository = UnitRepository(connection)
        units = repository.get_all()
        assert [unit.code for unit in units] == [
            "PCS", "DOZEN", "GRAM", "KG", "ML", "LITRE", "CARTON", "BOX", "PACK"
        ]
    finally:
        connection.close()


def test_unit_crud(tmp_path: Path):
    database_path = tmp_path / "test.db"
    initialize_database(database_path)
    connection = get_connection(database_path)
    try:
        repository = UnitRepository(connection)
        from domain.entities.unit import Unit
        unit = Unit("M", "Metre", "LENGTH", 1.0)
        repository.add(unit)
        assert unit.id is not None
        assert repository.get_by_code("m") == unit
        unit.name = "Meter"
        repository.update(unit)
        assert repository.get_by_id(unit.id) == unit
        repository.delete(unit.id)
        assert repository.get_by_code("M") is None
    finally:
        connection.close()
