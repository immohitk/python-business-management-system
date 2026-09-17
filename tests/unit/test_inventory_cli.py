from presentation.cli.inventory import handle_inventory, view_stock


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
