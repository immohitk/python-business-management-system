from pathlib import Path

from domain.entities.supplier import Supplier
from infrastructure.database.connection import get_connection
from infrastructure.database.initialization import initialize_database
from infrastructure.repositories.supplier_repository import SupplierRepository


def create_repository(tmp_path: Path) -> tuple[SupplierRepository, object]:
    database_path = tmp_path / "test.db"
    initialize_database(database_path)
    connection = get_connection(database_path)

    return SupplierRepository(connection), connection


def create_supplier() -> Supplier:
    return Supplier(
        id=None,
        name="ABC Paint Suppliers",
        phone="9876501234",
        email="abc@example.com",
        address="Delhi",
        created_at="2026-09-07T20:00:00",
    )


def test_add_supplier(tmp_path):
    repository, connection = create_repository(tmp_path)

    try:
        supplier = create_supplier()

        repository.add(supplier)

        assert supplier.id is not None
        assert supplier.id > 0
    finally:
        connection.close()


def test_get_supplier_by_id(tmp_path):
    repository, connection = create_repository(tmp_path)

    try:
        supplier = create_supplier()
        repository.add(supplier)

        result = repository.get_by_id(supplier.id)

        assert result == supplier
    finally:
        connection.close()


def test_get_supplier_by_id_returns_none_for_missing_supplier(tmp_path):
    repository, connection = create_repository(tmp_path)

    try:
        result = repository.get_by_id(999)

        assert result is None
    finally:
        connection.close()


def test_get_all_suppliers(tmp_path):
    repository, connection = create_repository(tmp_path)

    try:
        first_supplier = create_supplier()
        second_supplier = Supplier(
            id=None,
            name="XYZ Hardware Suppliers",
            phone="9123456780",
            email="xyz@example.com",
            address="Mumbai",
            created_at="2026-09-07T20:00:00",
        )

        repository.add(first_supplier)
        repository.add(second_supplier)

        result = repository.get_all()

        assert result == [first_supplier, second_supplier]
    finally:
        connection.close()


def test_delete_supplier(tmp_path):
    repository, connection = create_repository(tmp_path)

    try:
        supplier = create_supplier()
        repository.add(supplier)

        repository.delete(supplier.id)

        assert repository.get_by_id(supplier.id) is None
    finally:
        connection.close()