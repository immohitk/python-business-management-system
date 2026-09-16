from pathlib import Path

from application.services.inventory_service import InventoryService
from domain.entities.product import Product
from infrastructure.database.connection import get_connection
from infrastructure.database.initialization import initialize_database
from infrastructure.repositories.product_repository import ProductRepository
from infrastructure.repositories.stock_movement_repository import (
    StockMovementRepository,
)


def create_service(tmp_path: Path) -> tuple[InventoryService, ProductRepository, StockMovementRepository, object]:
    database_path = tmp_path / "test.db"
    initialize_database(database_path)
    connection = get_connection(database_path)

    product_repository = ProductRepository(connection)
    stock_movement_repository = StockMovementRepository(connection)
    service = InventoryService(
        product_repository,
        stock_movement_repository,
    )

    return service, product_repository, stock_movement_repository, connection


def create_product() -> Product:
    return Product(
        id=None,
        name="Paint",
        description="Interior wall paint",
        sku="PAINT-001",
        price=450.0,
        quantity=10,
        created_at="2026-09-16T20:00:00",
    )


def test_stock_in_increases_product_quantity(tmp_path):
    service, product_repository, _, connection = create_service(tmp_path)

    try:
        product = create_product()
        product_repository.add(product)

        service.stock_in(product.id, 5)

        result = product_repository.get_by_id(product.id)

        assert result is not None
        assert result.quantity == 15
    finally:
        connection.close()


def test_stock_in_creates_stock_movement(tmp_path):
    service, product_repository, stock_movement_repository, connection = create_service(
        tmp_path
    )

    try:
        product = create_product()
        product_repository.add(product)

        service.stock_in(product.id, 5)

        movements = stock_movement_repository.get_movements(product.id)

        assert len(movements) == 1
        assert movements[0].movement_type.value == "ADD"
        assert movements[0].quantity == 5
        assert movements[0].resulting_stock == 15
    finally:
        connection.close()


def test_stock_in_rejects_invalid_amount(tmp_path):
    service, product_repository, _, connection = create_service(tmp_path)

    try:
        product = create_product()
        product_repository.add(product)

        try:
            service.stock_in(product.id, 0)
        except ValueError as exc:
            assert str(exc) == "Stock addition amount must be greater than zero."
        else:
            raise AssertionError("Expected invalid stock-in amount to fail.")
    finally:
        connection.close()


def test_stock_in_rejects_missing_product(tmp_path):
    service, _, _, connection = create_service(tmp_path)

    try:
        try:
            service.stock_in(999, 5)
        except ValueError as exc:
            assert str(exc) == "Product not found."
        else:
            raise AssertionError("Expected missing product to fail.")
    finally:
        connection.close()
