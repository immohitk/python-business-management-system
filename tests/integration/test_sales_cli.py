from pathlib import Path

from application.services.inventory_service import InventoryService
from application.services.sale_service import SaleService
from domain.entities.product import Product
from infrastructure.database.connection import get_connection
from infrastructure.database.initialization import initialize_database
from infrastructure.repositories.product_repository import ProductRepository
from infrastructure.repositories.sale_repository import SaleRepository
from infrastructure.repositories.stock_movement_repository import (
    StockMovementRepository,
)
from presentation.cli.sales import create_sale


def create_database(tmp_path: Path):
    database_path = tmp_path / "sales_cli.db"
    initialize_database(database_path)
    return get_connection(database_path)


def create_sale_service(connection):
    sale_repository = SaleRepository(connection)
    product_repository = ProductRepository(connection)
    stock_movement_repository = StockMovementRepository(connection)

    inventory_service = InventoryService(
        product_repository,
        stock_movement_repository,
    )

    return (
        SaleService(
            sale_repository,
            inventory_service,
        ),
        sale_repository,
        product_repository,
        stock_movement_repository,
    )


def test_sale_cli_deducts_inventory_and_records_movement(
    tmp_path,
    monkeypatch,
    capsys,
) -> None:
    connection = create_database(tmp_path)

    try:
        (
            sale_service,
            sale_repository,
            product_repository,
            stock_movement_repository,
        ) = create_sale_service(connection)

        product = Product(
            id=None,
            name="CLI Sale Product",
            description="Sales CLI integration test",
            sku="SALE-CLI-001",
            price=500.0,
            quantity=10,
            created_at="2026-09-22T19:00:00",
        )

        product_repository.add(product)

        inputs = iter(
            [
                "1",
                "2026-09-22",
                str(product.id),
                "3",
                "500",
                "n",
            ]
        )

        monkeypatch.setattr(
            "builtins.input",
            lambda _: next(inputs),
        )

        create_sale(sale_service)

        captured = capsys.readouterr()

        assert "Sale created successfully" in captured.out
        assert "total: 1500.00" in captured.out

        stored_sale = sale_repository.get_by_id(1)

        assert stored_sale is not None
        assert stored_sale.customer_id == 1
        assert stored_sale.total_amount == 1500.0

        stored_product = product_repository.get_by_id(product.id)

        assert stored_product is not None
        assert stored_product.quantity == 7

        movements = stock_movement_repository.get_movements(product.id)

        assert len(movements) == 1
        assert movements[0].movement_type.value == "DEDUCT"
        assert movements[0].quantity == 3
        assert movements[0].resulting_stock == 7

    finally:
        connection.close()


def test_sale_cli_rolls_back_when_stock_is_insufficient(
    tmp_path,
    monkeypatch,
    capsys,
) -> None:
    connection = create_database(tmp_path)
    try:
        (
            sale_service,
            sale_repository,
            product_repository,
            stock_movement_repository,
        ) = create_sale_service(connection)

        product = Product(
            id=None,
            name="Limited Stock Product",
            description="Sales CLI rollback test",
            sku="SALE-CLI-002",
            price=500.0,
            quantity=2,
            created_at="2026-09-22T19:00:00",
        )
        product_repository.add(product)

        inputs = iter(
            [
                "1",
                "2026-09-22",
                str(product.id),
                "5",
                "500",
                "n",
            ]
        )
        monkeypatch.setattr(
            "builtins.input",
            lambda _: next(inputs),
        )

        create_sale(sale_service)

        captured = capsys.readouterr()

        assert "Stock quantity cannot be negative." in captured.out

        stored_sale = sale_repository.get_by_id(1)
        assert stored_sale is None

        stored_product = product_repository.get_by_id(product.id)
        assert stored_product is not None
        assert stored_product.quantity == 2

        movements = stock_movement_repository.get_movements(product.id)
        assert movements == []
    finally:
        connection.close()
