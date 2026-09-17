from unittest.mock import Mock

from presentation.cli.inventory import (
    adjust_stock,
    handle_inventory,
    stock_in,
    stock_out,
    view_movement_history,
    view_stock,
)


class FakeInventoryService:
    def __init__(self, products):
        self.products = products

    def get_stock(self):
        return self.products


def test_view_stock_displays_products(capsys):
    products = [
        type(
            "Product",
            (),
            {
                "id": 1,
                "name": "Paint",
                "sku": "PAINT-001",
                "quantity": 10,
            },
        )()
    ]

    service = FakeInventoryService(products)

    view_stock(service)

    captured = capsys.readouterr()

    assert "Current Stock" in captured.out
    assert "ID: 1" in captured.out
    assert "Name: Paint" in captured.out
    assert "SKU: PAINT-001" in captured.out
    assert "Quantity: 10" in captured.out


def test_view_stock_displays_no_products_message(capsys):
    service = FakeInventoryService([])

    view_stock(service)

    captured = capsys.readouterr()

    assert "Current Stock" in captured.out
    assert "No products found." in captured.out


def test_handle_inventory_view_stock(capsys, monkeypatch):
    products = [
        type(
            "Product",
            (),
            {
                "id": 1,
                "name": "Paint",
                "sku": "PAINT-001",
                "quantity": 10,
            },
        )()
    ]

    service = FakeInventoryService(products)

    choices = iter(["1", "0"])
    monkeypatch.setattr("builtins.input", lambda _: next(choices))

    handle_inventory(service)

    captured = capsys.readouterr()

    assert "Current Stock" in captured.out
    assert "Paint" in captured.out


def test_stock_in_calls_service(capsys, monkeypatch):
    service = Mock()

    inputs = iter(["1", "5"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    stock_in(service)

    service.stock_in.assert_called_once()

    call_args = service.stock_in.call_args

    assert call_args.args[0] == 1
    assert call_args.args[1] == 5
    assert isinstance(call_args.args[2], str)

    captured = capsys.readouterr()

    assert "Stock In" in captured.out
    assert "Stock added successfully." in captured.out


def test_handle_inventory_stock_in(capsys, monkeypatch):
    service = Mock()

    inputs = iter(["2", "1", "5", "0"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    handle_inventory(service)

    service.stock_in.assert_called_once()

    call_args = service.stock_in.call_args

    assert call_args.args[0] == 1
    assert call_args.args[1] == 5
    assert isinstance(call_args.args[2], str)

    captured = capsys.readouterr()

    assert "Stock In" in captured.out
    assert "Stock added successfully." in captured.out


def test_adjust_stock_calls_service(capsys, monkeypatch):
    service = Mock()

    inputs = iter(["1", "20"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    adjust_stock(service)

    service.adjust_stock.assert_called_once()

    call_args = service.adjust_stock.call_args

    assert call_args.args[0] == 1
    assert call_args.args[1] == 20
    assert isinstance(call_args.args[2], str)

    captured = capsys.readouterr()

    assert "Adjust Stock" in captured.out
    assert "Stock adjusted successfully." in captured.out


def test_handle_inventory_adjust_stock(capsys, monkeypatch):
    service = Mock()

    inputs = iter(["3", "1", "20", "0"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    handle_inventory(service)

    service.adjust_stock.assert_called_once()

    call_args = service.adjust_stock.call_args

    assert call_args.args[0] == 1
    assert call_args.args[1] == 20
    assert isinstance(call_args.args[2], str)

    captured = capsys.readouterr()

    assert "Adjust Stock" in captured.out
    assert "Stock adjusted successfully." in captured.out


def test_stock_out_calls_service(capsys, monkeypatch):
    service = Mock()

    inputs = iter(["1", "5"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    stock_out(service)

    service.stock_out.assert_called_once()

    call_args = service.stock_out.call_args

    assert call_args.args[0] == 1
    assert call_args.args[1] == 5
    assert isinstance(call_args.args[2], str)

    captured = capsys.readouterr()

    assert "Stock Out" in captured.out
    assert "Stock removed successfully." in captured.out


def test_handle_inventory_stock_out(capsys, monkeypatch):
    service = Mock()

    inputs = iter(["4", "1", "5", "0"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    handle_inventory(service)

    service.stock_out.assert_called_once()

    call_args = service.stock_out.call_args

    assert call_args.args[0] == 1
    assert call_args.args[1] == 5
    assert isinstance(call_args.args[2], str)

    captured = capsys.readouterr()

    assert "Stock Out" in captured.out
    assert "Stock removed successfully." in captured.out


def test_view_movement_history_displays_movements(capsys, monkeypatch) -> None:
    movement = Mock()
    movement.movement_type.value = "ADD"
    movement.quantity = 5
    movement.resulting_stock = 15
    movement.created_at = "2026-09-16T20:00:00"

    service = Mock()
    service.get_movement_history.return_value = [movement]

    monkeypatch.setattr("builtins.input", lambda _: "1")

    view_movement_history(service)

    output = capsys.readouterr().out

    assert "Stock Movement History" in output
    assert "Type: ADD" in output
    assert "Quantity: 5" in output
    assert "Resulting Stock: 15" in output
    assert "Created At: 2026-09-16T20:00:00" in output


def test_view_movement_history_displays_empty_message(capsys, monkeypatch) -> None:
    service = Mock()
    service.get_movement_history.return_value = []

    monkeypatch.setattr("builtins.input", lambda _: "1")

    view_movement_history(service)

    output = capsys.readouterr().out

    assert "No stock movements found." in output


def test_handle_inventory_movement_history(monkeypatch) -> None:
    service = Mock()
    movement = Mock()
    movement.movement_type.value = "ADD"
    movement.quantity = 5
    movement.resulting_stock = 15
    movement.created_at = "2026-09-16T20:00:00"
    service.get_movement_history.return_value = [movement]

    inputs = iter(["5", "1", "0"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    handle_inventory(service)

    service.get_movement_history.assert_called_once_with(1)
