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

        service.stock_in(
            product.id,
            5,
            created_at="2026-09-16T20:00:00",
        )

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

        service.stock_in(
            product.id,
            5,
            created_at="2026-09-16T20:00:00",
        )

        movements = stock_movement_repository.get_movements(product.id)

        assert len(movements) == 1
        assert movements[0].movement_type.value == "ADD"
        assert movements[0].quantity == 5
        assert movements[0].resulting_stock == 15
        assert movements[0].created_at == "2026-09-16T20:00:00"
    finally:
        connection.close()


def test_stock_in_rejects_invalid_amount(tmp_path):
    service, product_repository, _, connection = create_service(tmp_path)

    try:
        product = create_product()
        product_repository.add(product)

        try:
            service.stock_in(
                product.id,
                0,
                created_at="2026-09-16T20:00:00",
            )
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
            service.stock_in(
                999,
                5,
                created_at="2026-09-16T20:00:00",
            )
        except ValueError as exc:
            assert str(exc) == "Product not found."
        else:
            raise AssertionError("Expected missing product to fail.")
    finally:
        connection.close()


def test_adjust_stock_changes_product_quantity(tmp_path):
    service, product_repository, _, connection = create_service(tmp_path)

    try:
        product = create_product()
        product_repository.add(product)

        service.adjust_stock(
            product.id,
            20,
            created_at="2026-09-16T20:00:00",
        )

        result = product_repository.get_by_id(product.id)

        assert result is not None
        assert result.quantity == 20
    finally:
        connection.close()


def test_adjust_stock_creates_stock_movement(tmp_path):
    service, product_repository, stock_movement_repository, connection = create_service(
        tmp_path
    )

    try:
        product = create_product()
        product_repository.add(product)

        service.adjust_stock(
            product.id,
            20,
            created_at="2026-09-16T20:00:00",
        )

        movements = stock_movement_repository.get_movements(product.id)

        assert len(movements) == 1
        assert movements[0].movement_type.value == "ADJUST"
        assert movements[0].quantity == 20
        assert movements[0].resulting_stock == 20
        assert movements[0].created_at == "2026-09-16T20:00:00"
    finally:
        connection.close()


def test_adjust_stock_rejects_negative_quantity(tmp_path):
    service, product_repository, _, connection = create_service(tmp_path)

    try:
        product = create_product()
        product_repository.add(product)

        try:
            service.adjust_stock(
                product.id,
                -1,
                created_at="2026-09-16T20:00:00",
            )
        except ValueError as exc:
            assert str(exc) == "Stock quantity cannot be negative."
        else:
            raise AssertionError("Expected negative adjustment to fail.")
    finally:
        connection.close()


def test_adjust_stock_rejects_missing_product(tmp_path):
    service, _, _, connection = create_service(tmp_path)

    try:
        try:
            service.adjust_stock(
                999,
                20,
                created_at="2026-09-16T20:00:00",
            )
        except ValueError as exc:
            assert str(exc) == "Product not found."
        else:
            raise AssertionError("Expected missing product to fail.")
    finally:
        connection.close()


def test_stock_out_changes_product_quantity(tmp_path):
    service, product_repository, _, connection = create_service(tmp_path)
    try:
        product = create_product()
        product_repository.add(product)
        service.stock_out(
            product.id,
            3,
            created_at="2026-09-16T20:00:00",
        )

        result = product_repository.get_by_id(product.id)

        assert result is not None
        assert result.quantity == 7
    finally:
        connection.close()


def test_stock_out_creates_stock_movement(tmp_path):
    service, product_repository, stock_movement_repository, connection = create_service(
        tmp_path
    )
    try:
        product = create_product()
        product_repository.add(product)
        service.stock_out(
            product.id,
            3,
            created_at="2026-09-16T20:00:00",
        )

        movements = stock_movement_repository.get_movements(product.id)

        assert len(movements) == 1
        assert movements[0].movement_type.value == "DEDUCT"
        assert movements[0].quantity == 3
        assert movements[0].resulting_stock == 7
        assert movements[0].created_at == "2026-09-16T20:00:00"
    finally:
        connection.close()


def test_stock_out_rejects_zero_amount(tmp_path):
    service, product_repository, _, connection = create_service(tmp_path)
    try:
        product = create_product()
        product_repository.add(product)

        try:
            service.stock_out(
                product.id,
                0,
                created_at="2026-09-16T20:00:00",
            )
        except ValueError as exc:
            assert str(exc) == "Stock deduction amount must be greater than zero."
        else:
            raise AssertionError("Expected zero stock-out to fail.")
    finally:
        connection.close()


def test_stock_out_rejects_insufficient_stock(tmp_path):
    service, product_repository, stock_movement_repository, connection = create_service(
        tmp_path
    )
    try:
        product = create_product()
        product_repository.add(product)

        try:
            service.stock_out(
                product.id,
                11,
                created_at="2026-09-16T20:00:00",
            )
        except ValueError as exc:
            assert str(exc) == "Stock quantity cannot be negative."
        else:
            raise AssertionError("Expected insufficient stock to fail.")

        result = product_repository.get_by_id(product.id)
        assert result is not None
        assert result.quantity == 10
        assert stock_movement_repository.get_movements(product.id) == []
    finally:
        connection.close()


def test_stock_out_rejects_missing_product(tmp_path):
    service, _, _, connection = create_service(tmp_path)
    try:
        try:
            service.stock_out(
                999,
                3,
                created_at="2026-09-16T20:00:00",
            )
        except ValueError as exc:
            assert str(exc) == "Product not found."
        else:
            raise AssertionError("Expected missing product to fail.")
    finally:
        connection.close()
