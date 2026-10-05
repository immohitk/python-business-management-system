
from pathlib import Path

from infrastructure.database.connection import get_connection
from infrastructure.database.initialization import initialize_database
from infrastructure.repositories.supplier_product_repository import SupplierProductRepository


def create_repository(tmp_path: Path):
    database_path = tmp_path / "supplier_product.db"
    initialize_database(database_path)
    connection = get_connection(database_path)
    return SupplierProductRepository(connection), connection


def seed_supplier_and_product(connection):
    supplier = connection.execute(
        "INSERT INTO suppliers (name, phone, email, address, created_at) VALUES (?, ?, ?, ?, ?)",
        ("Supplier A", "111", "a@example.com", "Delhi", "2026-10-05T10:00:00"),
    ).lastrowid
    product = connection.execute(
        "INSERT INTO products (name, description, sku, price, quantity, created_at) VALUES (?, ?, ?, ?, ?, ?)",
        ("Paint", "Wall paint", "PAINT-001", 450, 10, "2026-10-05T10:00:00"),
    ).lastrowid
    connection.commit()
    return supplier, product


def test_supplier_can_supply_multiple_products(tmp_path):
    repository, connection = create_repository(tmp_path)
    try:
        supplier, product_one = seed_supplier_and_product(connection)
        product_two = connection.execute(
            "INSERT INTO products (name, description, sku, price, quantity, created_at) VALUES (?, ?, ?, ?, ?, ?)",
            ("Brush", "Paint brush", "BRUSH-001", 120, 5, "2026-10-05T10:00:00"),
        ).lastrowid
        connection.commit()

        repository.add(supplier, product_one)
        repository.add(supplier, product_two)

        assert repository.get_product_ids_for_supplier(supplier) == [product_one, product_two]
    finally:
        connection.close()


def test_product_can_have_multiple_suppliers(tmp_path):
    repository, connection = create_repository(tmp_path)
    try:
        supplier_one, product = seed_supplier_and_product(connection)
        supplier_two = connection.execute(
            "INSERT INTO suppliers (name, phone, email, address, created_at) VALUES (?, ?, ?, ?, ?)",
            ("Supplier B", "222", "b@example.com", "Mumbai", "2026-10-05T10:00:00"),
        ).lastrowid
        connection.commit()

        repository.add(supplier_one, product)
        repository.add(supplier_two, product)

        assert repository.get_supplier_ids_for_product(product) == [supplier_one, supplier_two]
    finally:
        connection.close()


def test_duplicate_supplier_product_assignment_is_idempotent(tmp_path):
    repository, connection = create_repository(tmp_path)
    try:
        supplier, product = seed_supplier_and_product(connection)
        repository.add(supplier, product)
        repository.add(supplier, product)

        assert repository.get_supplier_ids_for_product(product) == [supplier]
        assert repository.exists(supplier, product)
    finally:
        connection.close()


def test_remove_supplier_from_product(tmp_path):
    repository, connection = create_repository(tmp_path)
    try:
        supplier, product = seed_supplier_and_product(connection)
        repository.add(supplier, product)
        repository.remove(supplier, product)

        assert repository.get_supplier_ids_for_product(product) == []
        assert not repository.exists(supplier, product)
    finally:
        connection.close()
