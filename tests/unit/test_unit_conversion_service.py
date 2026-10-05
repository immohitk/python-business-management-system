from pathlib import Path

import pytest

from application.services.unit_conversion_service import UnitConversionService
from infrastructure.database.connection import get_connection
from infrastructure.database.initialization import initialize_database
from infrastructure.repositories.unit_repository import UnitRepository


def create_service(tmp_path: Path):
    database_path = tmp_path / "test.db"
    initialize_database(database_path)
    connection = get_connection(database_path)
    return UnitConversionService(UnitRepository(connection)), connection


def test_mass_conversion(tmp_path):
    service, connection = create_service(tmp_path)
    try:
        assert service.convert(2, "KG", "GRAM") == 2000
        assert service.convert(2500, "GRAM", "KG") == 2.5
    finally:
        connection.close()


def test_volume_conversion(tmp_path):
    service, connection = create_service(tmp_path)
    try:
        assert service.convert(3, "LITRE", "ML") == 3000
    finally:
        connection.close()


def test_count_conversion(tmp_path):
    service, connection = create_service(tmp_path)
    try:
        assert service.convert(2, "DOZEN", "PCS") == 24
        assert service.convert(24, "PCS", "DOZEN") == 2
    finally:
        connection.close()


def test_rejects_incompatible_units(tmp_path):
    service, connection = create_service(tmp_path)
    try:
        with pytest.raises(ValueError, match="different dimensions"):
            service.convert(1, "KG", "LITRE")
    finally:
        connection.close()
