from pathlib import Path

from application.services.inventory_service import InventoryService
from domain.entities.product import Product
from infrastructure.database.connection import get_connection
from infrastructure.database.initialization import initialize_database
from infrastructure.repositories.product_repository import ProductRepository
from infrastructure.repositories.stock_movement_repository import (
    StockMovementRepository,
)
from presentation.cli.inventory import (
    adjust_stock,
    stock_in,
    stock_out,
    view_movement_history,
    view_stock,
)


def create_database(tmp_path: Path):
    database_path = tmp_path / "inventory_cli.db"
    initialize_database(database_path)
    return get_connection(database_path)


def test_inventory_cli_persists_complete_stock_workflow(
    tmp_path,
    monkeypatch,
    capsys,
) -> None:
    connection = create_database(tmp_path)

    try:
        product_repository = ProductRepository(connection)
        stock_movement_repository = StockMovementRepository(connection)

        inventory_service = InventoryService(
            product_repository,
            stock_movement_repository,
        )

        product = Product(
            id=None,
            name="CLI Integration Product",
            description="Inventory CLI integration test",
            sku="CLI-001",
            price=500.0,
            quantity=20,
            created_at="2026-09-18T10:00:00",
        )

        product_repository.add(product)

        inputs = iter(
            [
                str(product.id),
                "5",
            ]
        )
        monkeypatch.setattr(
            "builtins.input",
            lambda _: next(inputs),
        )

        stock_in(inventory_service)

        captured = capsys.readouterr()
        assert "Stock added successfully." in captured.out

        inputs = iter(
            [
                str(product.id),
                "12",
            ]
        )
        monkeypatch.setattr(
            "builtins.input",
            lambda _: next(inputs),
        )

        adjust_stock(inventory_service)

        captured = capsys.readouterr()
        assert "Stock adjusted successfully." in captured.out

        inputs = iter(
            [
                str(product.id),
                "4",
            ]
        )
        monkeypatch.setattr(
            "builtins.input",
            lambda _: next(inputs),
        )

        stock_out(inventory_service)

        captured = capsys.readouterr()
        assert "Stock removed successfully." in captured.out

        view_stock(inventory_service)

        captured = capsys.readouterr()
        assert "CLI Integration Product" in captured.out
        assert "8" in captured.out

        inputs = iter([str(product.id)])
        monkeypatch.setattr(
            "builtins.input",
            lambda _: next(inputs),
        )

        view_movement_history(inventory_service)

        captured = capsys.readouterr()

        assert "ADD" in captured.out
        assert "ADJUST" in captured.out
        assert "DEDUCT" in captured.out

        result = product_repository.get_by_id(product.id)

        assert result is not None
        assert result.quantity == 8

        movements = stock_movement_repository.get_movements(product.id)

        assert len(movements) == 3
        assert movements[0].quantity == 5
        assert movements[0].resulting_stock == 25
        assert movements[1].quantity == 12
        assert movements[1].resulting_stock == 12
        assert movements[2].quantity == 4
        assert movements[2].resulting_stock == 8

        assert all(movement.created_at for movement in movements)

    finally:
        connection.close()
