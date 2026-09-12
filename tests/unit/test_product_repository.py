import sqlite3
from pathlib import Path

from infrastructure.database.connection import get_connection
from infrastructure.database.initialization import initialize_database
from infrastructure.repositories.product_repository import ProductRepository
from domain.entities.product import Product


def create_repository(tmp_path: Path) -> tuple[ProductRepository, object]:
    database_path = tmp_path / "test.db"
    initialize_database(database_path)
    connection = get_connection(database_path)

    return ProductRepository(connection), connection


def create_product() -> Product:
    return Product(
        id=None,
        name="Paint",
        description="Interior wall paint",
        sku="PAINT-001",
        price=450.0,
        quantity=10,
        created_at="2026-09-07T20:00:00",
    )


def test_add_product(tmp_path):
    repository, connection = create_repository(tmp_path)

    try:
        product = create_product()

        repository.add(product)

        assert product.id is not None
        assert product.id > 0
    finally:
        connection.close()


def test_get_product_by_id(tmp_path):
    repository, connection = create_repository(tmp_path)

    try:
        product = create_product()
        repository.add(product)

        result = repository.get_by_id(product.id)

        assert result == product
    finally:
        connection.close()


def test_get_product_by_id_returns_none_for_missing_product(tmp_path):
    repository, connection = create_repository(tmp_path)

    try:
        result = repository.get_by_id(999)

        assert result is None
    finally:
        connection.close()


def test_get_all_products(tmp_path):
    repository, connection = create_repository(tmp_path)

    try:
        first_product = create_product()
        second_product = Product(
            id=None,
            name="Brush",
            description="Paint brush",
            sku="BRUSH-001",
            price=120.0,
            quantity=20,
            created_at="2026-09-07T20:00:00",
        )

        repository.add(first_product)
        repository.add(second_product)

        result = repository.get_all()

        assert result == [first_product, second_product]
    finally:
        connection.close()


def test_delete_product(tmp_path):
    repository, connection = create_repository(tmp_path)

    try:
        product = create_product()
        repository.add(product)

        repository.delete(product.id)

        assert repository.get_by_id(product.id) is None
    finally:
        connection.close()


def test_add_product_with_no_description(tmp_path):
    repository, connection = create_repository(tmp_path)

    try:
        product = Product(
            id=None,
            name="Primer",
            description=None,
            sku="PRIMER-001",
            price=300.0,
            quantity=5,
            created_at="2026-09-12T10:00:00",
        )

        repository.add(product)

        result = repository.get_by_id(product.id)

        assert result == product
    finally:
        connection.close()


def test_add_product_with_zero_price_and_quantity(tmp_path):
    repository, connection = create_repository(tmp_path)

    try:
        product = Product(
            id=None,
            name="Sample Product",
            description="Test product",
            sku="SAMPLE-001",
            price=0.0,
            quantity=0,
            created_at="2026-09-12T10:00:00",
        )

        repository.add(product)

        result = repository.get_by_id(product.id)

        assert result == product
    finally:
        connection.close()


def test_add_product_with_duplicate_sku_fails(tmp_path):
    repository, connection = create_repository(tmp_path)

    try:
        first_product = create_product()
        second_product = Product(
            id=None,
            name="Another Paint",
            description="Another product",
            sku="PAINT-001",
            price=500.0,
            quantity=5,
            created_at="2026-09-12T10:00:00",
        )

        repository.add(first_product)

        try:
            repository.add(second_product)
        except sqlite3.IntegrityError:
            pass
        else:
            raise AssertionError("Expected duplicate SKU to fail.")
    finally:
        connection.close()
