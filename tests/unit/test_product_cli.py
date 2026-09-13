from presentation.cli.products import (
    add_product,
    delete_product,
    get_product,
    list_products,
)


class FakeProductService:
    def __init__(self):
        self.added_product = None

    def add_product(self, product):
        product.id = 1
        self.added_product = product


def test_add_product_creates_and_persists_product(monkeypatch, capsys):
    repository = FakeProductService()
    inputs = iter(
        [
            "Interior Paint",
            "White wall paint",
            "PAINT-CLI-001",
            "850",
            "25",
        ]
    )

    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    add_product(repository)

    captured = capsys.readouterr()

    assert repository.added_product is not None
    assert repository.added_product.name == "Interior Paint"
    assert repository.added_product.description == "White wall paint"
    assert repository.added_product.sku == "PAINT-CLI-001"
    assert repository.added_product.price == 850.0
    assert repository.added_product.quantity == 25
    assert repository.added_product.id == 1
    assert "Product added successfully with ID: 1" in captured.out


from domain.entities.product import Product
from presentation.cli.products import list_products


def test_list_products_displays_products(capsys):
    product = Product(
        id=1,
        name="Interior Paint",
        description="White wall paint",
        sku="PAINT-CLI-001",
        price=850.0,
        quantity=25,
        created_at="2026-08-09T10:00:00",
    )

    class FakeProductService:
        def get_products(self):
            return [product]

    service = FakeProductService()

    list_products(service)

    captured = capsys.readouterr()

    assert "Product List" in captured.out
    assert "ID: 1" in captured.out
    assert "Name: Interior Paint" in captured.out
    assert "SKU: PAINT-CLI-001" in captured.out
    assert "Price: 850.00" in captured.out
    assert "Quantity: 25" in captured.out


def test_get_product_displays_product(capsys, monkeypatch):
    product = Product(
        id=1,
        name="Interior Paint",
        description="White wall paint",
        sku="PAINT-CLI-001",
        price=850.0,
        quantity=25,
        created_at="2026-08-09T10:00:00",
    )

    class FakeProductService:
        def get_product(self, product_id):
            assert product_id == 1
            return product

    monkeypatch.setattr("builtins.input", lambda _: "1")

    service = FakeProductService()

    get_product(service)

    captured = capsys.readouterr()

    assert "Get Product" in captured.out
    assert "ID: 1" in captured.out
    assert "Name: Interior Paint" in captured.out
    assert "SKU: PAINT-CLI-001" in captured.out
    assert "Price: 850.00" in captured.out
    assert "Quantity: 25" in captured.out


def test_delete_product_deletes_product(capsys, monkeypatch):
    class FakeProductService:
        def __init__(self):
            self.deleted_product_id = None

        def delete_product(self, product_id):
            self.deleted_product_id = product_id

    service = FakeProductService()

    monkeypatch.setattr("builtins.input", lambda _: "1")

    delete_product(service)

    captured = capsys.readouterr()

    assert service.deleted_product_id == 1
    assert "Delete Product" in captured.out
    assert "Product deleted successfully with ID: 1" in captured.out
