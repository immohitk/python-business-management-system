from pathlib import Path
from unittest.mock import Mock, patch

from application.services.inventory_service import InventoryService
from application.services.sale_service import SaleService
from domain.entities.product import Product
from domain.entities.sale import Sale
from infrastructure.database.connection import get_connection
from infrastructure.database.initialization import initialize_database
from infrastructure.repositories.product_repository import ProductRepository
from infrastructure.repositories.sale_repository import SaleRepository
from infrastructure.repositories.stock_movement_repository import (
    StockMovementRepository,
)
from presentation.cli.sales import (
    create_sale,
    create_sale_service,
    handle_sales,
    list_sales,
)


def test_create_sale_service_builds_sale_service():
    service, connection = create_sale_service()

    try:
        assert service.sale_repository is not None
        assert service.inventory_service is not None
        assert service.sale_repository.connection is connection
    finally:
        connection.close()


@patch("presentation.cli.sales.create_sale_service")
def test_handle_sales_back(mock_create_service):
    service = Mock()
    connection = Mock()
    mock_create_service.return_value = service, connection

    with patch("builtins.input", return_value="0"):
        handle_sales()

    mock_create_service.assert_called_once()
    connection.close.assert_called_once()


def test_handle_sales_accepts_injected_service():
    service = Mock()

    with patch("builtins.input", side_effect=["0"]):
        handle_sales(service)


def test_create_sale_creates_single_line_sale(capsys):
    service = Mock()

    with patch(
        "builtins.input",
        side_effect=[
            "1",
            "2026-09-22",
            "1",
            "2",
            "1000",
            "n",
        ],
    ):
        create_sale(service)

    sale = service.create_sale.call_args.args[0]

    assert isinstance(sale, Sale)
    assert sale.customer_id == 1
    assert sale.sale_date == "2026-09-22"
    assert len(sale.lines) == 1
    assert sale.lines[0].product_id == 1
    assert sale.lines[0].quantity == 2
    assert sale.lines[0].unit_price == 1000.0

    captured = capsys.readouterr()

    assert "Create Sale" in captured.out


def test_create_sale_creates_multiple_lines(capsys):
    service = Mock()

    with patch(
        "builtins.input",
        side_effect=[
            "1",
            "2026-09-22",
            "1",
            "2",
            "1000",
            "y",
            "2",
            "3",
            "500",
            "n",
        ],
    ):
        create_sale(service)

    sale = service.create_sale.call_args.args[0]

    assert len(sale.lines) == 2

    assert sale.lines[0].product_id == 1
    assert sale.lines[0].quantity == 2
    assert sale.lines[0].unit_price == 1000.0

    assert sale.lines[1].product_id == 2
    assert sale.lines[1].quantity == 3
    assert sale.lines[1].unit_price == 500.0


def test_create_sale_prints_success_message(capsys):
    service = Mock()

    def create_sale_side_effect(sale):
        sale.id = 10
        sale.apply_calculated_total()

    service.create_sale.side_effect = create_sale_side_effect

    with patch(
        "builtins.input",
        side_effect=[
            "1",
            "2026-09-22",
            "1",
            "2",
            "1000",
            "n",
        ],
    ):
        create_sale(service)

    captured = capsys.readouterr()

    assert "Sale created successfully with ID: 10" in captured.out
    assert "total: 2000.00" in captured.out


def test_create_sale_handles_invalid_customer_id(capsys):
    service = Mock()

    with patch(
        "builtins.input",
        side_effect=[
            "0",
            "2026-09-22",
            "1",
            "1",
            "1000",
            "n",
        ],
    ):
        create_sale(service)

    captured = capsys.readouterr()

    assert "Sale customer ID must be greater than zero" in captured.out
    service.create_sale.assert_not_called()


def test_create_sale_handles_invalid_sale_line(capsys):
    service = Mock()

    with patch(
        "builtins.input",
        side_effect=[
            "1",
            "2026-09-22",
            "1",
            "0",
            "1000",
            "n",
        ],
    ):
        create_sale(service)

    captured = capsys.readouterr()

    assert "Sale line quantity must be greater than zero" in captured.out
    service.create_sale.assert_not_called()


def test_create_sale_integrates_with_sale_service_and_inventory(
    tmp_path: Path,
    capsys,
):
    database_path = tmp_path / "test.db"
    initialize_database(database_path)

    connection = get_connection(database_path)

    try:
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

        product = Product(
            id=None,
            name="Paint",
            description="Interior wall paint",
            sku="PAINT-001",
            price=450.0,
            quantity=10,
            created_at="2026-09-22T18:00:00",
        )

        product_repository.add(product)

        with patch(
            "builtins.input",
            side_effect=[
                "1",
                "2026-09-22",
                str(product.id),
                "2",
                "450",
                "n",
            ],
        ):
            create_sale(service)

        stored_sale = sale_repository.get_by_id(1)
        stored_product = product_repository.get_by_id(product.id)

        assert stored_sale is not None
        assert stored_sale.customer_id == 1
        assert stored_sale.total_amount == 900.0

        assert stored_product is not None
        assert stored_product.quantity == 8

        movements = stock_movement_repository.get_movements(product.id)

        assert len(movements) == 1
        assert movements[0].movement_type.value == "DEDUCT"
        assert movements[0].quantity == 2
        assert movements[0].resulting_stock == 8

        captured = capsys.readouterr()

        assert "Sale created successfully" in captured.out
        assert "total: 900.00" in captured.out
    finally:
        connection.close()


def test_list_sales_prints_sales(capsys):
    service = Mock()
    service.get_sales.return_value = [
        Sale(
            id=1,
            customer_id=1,
            sale_date="2026-09-22",
            total_amount=900.0,
            created_at="2026-09-22T18:00:00",
            lines=[],
        ),
        Sale(
            id=2,
            customer_id=2,
            sale_date="2026-09-23",
            total_amount=1500.0,
            created_at="2026-09-23T18:00:00",
            lines=[],
        ),
    ]

    list_sales(service)

    captured = capsys.readouterr()

    assert "Sales List" in captured.out
    assert "ID: 1" in captured.out
    assert "Customer ID: 1" in captured.out
    assert "Sale Date: 2026-09-22" in captured.out
    assert "Total: 900.00" in captured.out
    assert "ID: 2" in captured.out
    assert "Customer ID: 2" in captured.out
    assert "Sale Date: 2026-09-23" in captured.out
    assert "Total: 1500.00" in captured.out


def test_list_sales_prints_empty_message(capsys):
    service = Mock()
    service.get_sales.return_value = []

    list_sales(service)

    captured = capsys.readouterr()

    assert "Sales List" in captured.out
    assert "No sales found." in captured.out


def test_handle_sales_lists_sales(capsys):
    service = Mock()
    service.get_sales.return_value = [
        Sale(
            id=1,
            customer_id=1,
            sale_date="2026-09-22",
            total_amount=900.0,
            created_at="2026-09-22T18:00:00",
            lines=[],
        )
    ]

    with patch(
        "builtins.input",
        side_effect=["2", "0"],
    ):
        handle_sales(service)

    captured = capsys.readouterr()

    assert "Sales List" in captured.out
    assert "ID: 1" in captured.out
    assert "Total: 900.00" in captured.out
    service.get_sales.assert_called_once()


def test_list_sales_integrates_with_database(tmp_path, capsys):
    database_path = tmp_path / "test.db"
    initialize_database(database_path)
    connection = get_connection(database_path)

    try:
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

        sale = Sale(
            id=None,
            customer_id=5,
            sale_date="2026-09-22",
            total_amount=1250.0,
            created_at="2026-09-22T19:00:00",
            lines=[],
        )

        sale_repository.add(sale)

        list_sales(service)

        captured = capsys.readouterr()

        assert "Sales List" in captured.out
        assert f"ID: {sale.id}" in captured.out
        assert "Customer ID: 5" in captured.out
        assert "Sale Date: 2026-09-22" in captured.out
        assert "Total: 1250.00" in captured.out
    finally:
        connection.close()
