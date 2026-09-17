from unittest.mock import Mock

from presentation.cli.inventory import (
    adjust_stock,
    handle_inventory,
    stock_in,
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
