from pathlib import Path

from application.services.inventory_service import InventoryService
from application.services.sale_service import SaleService
from domain.entities.product import Product
from domain.entities.sale import Sale
from domain.entities.sale_line import SaleLine
from infrastructure.database.connection import get_connection
from infrastructure.database.initialization import initialize_database
from infrastructure.repositories.product_repository import ProductRepository
from infrastructure.repositories.sale_repository import SaleRepository
from infrastructure.repositories.stock_movement_repository import (
    StockMovementRepository,
)


def create_service(
    tmp_path: Path,
) -> tuple[
    SaleService,
    SaleRepository,
    ProductRepository,
    StockMovementRepository,
    object,
]:
    database_path = tmp_path / "test.db"
    initialize_database(database_path)
    connection = get_connection(database_path)

    sale_repository = SaleRepository(connection)
    product_repository = ProductRepository(connection)
    stock_movement_repository = StockMovementRepository(connection)

    inventory_service = InventoryService(
        product_repository,
        stock_movement_repository,
    )

    service = SaleService(
        sale_repository,
        inventory_service,
    )

    return (
        service,
        sale_repository,
        product_repository,
        stock_movement_repository,
        connection,
    )


def create_products(product_repository: ProductRepository) -> None:
    product_repository.add(
        Product(
            id=None,
            name="Paint",
            description="Interior wall paint",
            sku="PAINT-001",
            price=450.0,
            quantity=10,
            created_at="2026-09-21T20:00:00",
        )
    )

    product_repository.add(
        Product(
            id=None,
            name="Brush",
            description="Paint brush",
            sku="BRUSH-001",
            price=120.0,
            quantity=10,
            created_at="2026-09-21T20:00:00",
        )
    )


def create_sale() -> Sale:
    return Sale(
        id=None,
        customer_id=1,
        sale_date="2026-09-21",
        total_amount=0.0,
        created_at="2026-09-21T20:00:00",
        lines=[
            SaleLine(
                product_id=1,
                quantity=2,
                unit_price=100.0,
            ),
            SaleLine(
                product_id=2,
                quantity=3,
                unit_price=50.0,
            ),
        ],
    )


def test_create_sale_persists_sale(tmp_path):
    (
        service,
        sale_repository,
        product_repository,
        _,
        connection,
    ) = create_service(tmp_path)

    try:
        create_products(product_repository)

        sale = create_sale()

        result = service.create_sale(sale)

        assert result.id is not None

        stored_sale = sale_repository.get_by_id(result.id)

        assert stored_sale is not None
        assert stored_sale.customer_id == 1
        assert stored_sale.total_amount == 350.0
    finally:
        connection.close()


def test_create_sale_persists_sale_items(tmp_path):
    (
        service,
        sale_repository,
        product_repository,
        _,
        connection,
    ) = create_service(tmp_path)

    try:
        create_products(product_repository)

        sale = create_sale()

        result = service.create_sale(sale)

        assert result.id is not None

        items = sale_repository.get_items(result.id)

        assert len(items) == 2

        assert items[0].product_id == 1
        assert items[0].quantity == 2
        assert items[0].unit_price == 100.0

        assert items[1].product_id == 2
        assert items[1].quantity == 3
        assert items[1].unit_price == 50.0
    finally:
        connection.close()


def test_create_sale_applies_calculated_total(tmp_path):
    (
        service,
        _,
        product_repository,
        _,
        connection,
    ) = create_service(tmp_path)

    try:
        create_products(product_repository)

        sale = create_sale()

        assert sale.total_amount == 0.0

        result = service.create_sale(sale)

        assert result.total_amount == 350.0
    finally:
        connection.close()


def test_create_sale_reconstructs_sale_lines(tmp_path):
    (
        service,
        sale_repository,
        product_repository,
        _,
        connection,
    ) = create_service(tmp_path)

    try:
        create_products(product_repository)

        sale = create_sale()

        result = service.create_sale(sale)

        stored_sale = sale_repository.get_by_id(result.id)

        assert stored_sale is not None
        assert len(stored_sale.lines) == 2

        assert stored_sale.lines[0].product_id == 1
        assert stored_sale.lines[0].quantity == 2
        assert stored_sale.lines[0].unit_price == 100.0

        assert stored_sale.lines[1].product_id == 2
        assert stored_sale.lines[1].quantity == 3
        assert stored_sale.lines[1].unit_price == 50.0
    finally:
        connection.close()


def test_create_sale_without_lines_persists_zero_total(tmp_path):
    (
        service,
        sale_repository,
        _,
        _,
        connection,
    ) = create_service(tmp_path)

    try:
        sale = Sale(
            id=None,
            customer_id=1,
            sale_date="2026-09-21",
            total_amount=0.0,
            created_at="2026-09-21T20:00:00",
            lines=[],
        )

        result = service.create_sale(sale)

        assert result.id is not None
        assert result.total_amount == 0.0

        stored_sale = sale_repository.get_by_id(result.id)

        assert stored_sale is not None
        assert stored_sale.lines == []
    finally:
        connection.close()


def test_create_sale_deducts_product_stock(tmp_path):
    (
        service,
        _,
        product_repository,
        _,
        connection,
    ) = create_service(tmp_path)

    try:
        create_products(product_repository)

        sale = create_sale()

        service.create_sale(sale)

        first_product = product_repository.get_by_id(1)
        second_product = product_repository.get_by_id(2)

        assert first_product is not None
        assert second_product is not None

        assert first_product.quantity == 8
        assert second_product.quantity == 7
    finally:
        connection.close()


def test_create_sale_creates_deduct_movements(tmp_path):
    (
        service,
        _,
        product_repository,
        stock_movement_repository,
        connection,
    ) = create_service(tmp_path)

    try:
        create_products(product_repository)

        sale = create_sale()

        service.create_sale(sale)

        first_movements = stock_movement_repository.get_movements(1)
        second_movements = stock_movement_repository.get_movements(2)

        assert len(first_movements) == 1
        assert first_movements[0].movement_type.value == "DEDUCT"
        assert first_movements[0].quantity == 2
        assert first_movements[0].resulting_stock == 8
        assert first_movements[0].created_at == sale.created_at

        assert len(second_movements) == 1
        assert second_movements[0].movement_type.value == "DEDUCT"
        assert second_movements[0].quantity == 3
        assert second_movements[0].resulting_stock == 7
        assert second_movements[0].created_at == sale.created_at
    finally:
        connection.close()


def test_create_sale_rejects_insufficient_stock(tmp_path):
    (
        service,
        sale_repository,
        product_repository,
        stock_movement_repository,
        connection,
    ) = create_service(tmp_path)

    try:
        create_products(product_repository)

        sale = Sale(
            id=None,
            customer_id=1,
            sale_date="2026-09-21",
            total_amount=0.0,
            created_at="2026-09-21T20:00:00",
            lines=[
                SaleLine(
                    product_id=1,
                    quantity=11,
                    unit_price=100.0,
                )
            ],
        )

        try:
            service.create_sale(sale)
        except ValueError as exc:
            assert str(exc) == "Stock quantity cannot be negative."
        else:
            raise AssertionError("Expected insufficient stock to fail.")

        product = product_repository.get_by_id(1)

        assert product is not None
        assert product.quantity == 10
        assert stock_movement_repository.get_movements(1) == []

        assert sale.id is not None

        stored_sale = sale_repository.get_by_id(sale.id)

        assert stored_sale is None
    finally:
        connection.close()


def test_create_sale_rolls_back_sale_items_and_stock_on_failure(tmp_path):
    (
        service,
        sale_repository,
        product_repository,
        stock_movement_repository,
        connection,
    ) = create_service(tmp_path)

    try:
        create_products(product_repository)

        sale = Sale(
            id=None,
            customer_id=1,
            sale_date="2026-09-21",
            total_amount=0.0,
            created_at="2026-09-21T20:00:00",
            lines=[
                SaleLine(
                    product_id=1,
                    quantity=2,
                    unit_price=100.0,
                ),
                SaleLine(
                    product_id=2,
                    quantity=11,
                    unit_price=50.0,
                ),
            ],
        )

        try:
            service.create_sale(sale)
        except ValueError as exc:
            assert str(exc) == "Stock quantity cannot be negative."
        else:
            raise AssertionError("Expected insufficient stock to fail.")

        assert sale.id is not None

        assert sale_repository.get_by_id(sale.id) is None
        assert sale_repository.get_items(sale.id) == []

        first_product = product_repository.get_by_id(1)
        second_product = product_repository.get_by_id(2)

        assert first_product is not None
        assert second_product is not None

        assert first_product.quantity == 10
        assert second_product.quantity == 10

        assert stock_movement_repository.get_movements(1) == []
        assert stock_movement_repository.get_movements(2) == []
    finally:
        connection.close()


def test_get_sales_returns_all_sales(tmp_path):
    (
        service,
        sale_repository,
        _,
        _,
        connection,
    ) = create_service(tmp_path)

    try:
        first_sale = Sale(
            id=None,
            customer_id=1,
            sale_date="2026-09-21",
            total_amount=100.0,
            created_at="2026-09-21T20:00:00",
            lines=[],
        )
        second_sale = Sale(
            id=None,
            customer_id=2,
            sale_date="2026-09-22",
            total_amount=200.0,
            created_at="2026-09-22T20:00:00",
            lines=[],
        )

        sale_repository.add(first_sale)
        sale_repository.add(second_sale)

        sales = service.get_sales()

        assert len(sales) == 2
        assert sales[0].id == first_sale.id
        assert sales[0].customer_id == 1
        assert sales[0].total_amount == 100.0
        assert sales[1].id == second_sale.id
        assert sales[1].customer_id == 2
        assert sales[1].total_amount == 200.0
    finally:
        connection.close()
