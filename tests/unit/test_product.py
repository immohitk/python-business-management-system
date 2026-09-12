import pytest

from domain.entities.product import Product


def test_valid_product_can_be_created():
    product = Product(
        id=None,
        name="Interior Paint",
        description="White wall paint",
        sku="PAINT-001",
        price=850.0,
        quantity=25,
        created_at="2026-09-12T19:00:00",
    )

    assert product.name == "Interior Paint"
    assert product.sku == "PAINT-001"
    assert product.price == 850.0
    assert product.quantity == 25


def test_product_name_cannot_be_empty():
    with pytest.raises(ValueError, match="Product name cannot be empty"):
        Product(
            id=None,
            name="",
            description=None,
            sku="PAINT-001",
            price=850.0,
            quantity=25,
            created_at="2026-09-12T19:00:00",
        )


def test_product_sku_cannot_be_empty():
    with pytest.raises(ValueError, match="Product SKU cannot be empty"):
        Product(
            id=None,
            name="Interior Paint",
            description=None,
            sku="",
            price=850.0,
            quantity=25,
            created_at="2026-09-12T19:00:00",
        )


def test_product_price_cannot_be_negative():
    with pytest.raises(ValueError, match="Product price cannot be negative"):
        Product(
            id=None,
            name="Interior Paint",
            description=None,
            sku="PAINT-001",
            price=-100.0,
            quantity=25,
            created_at="2026-09-12T19:00:00",
        )


def test_product_quantity_cannot_be_negative():
    with pytest.raises(ValueError, match="Product quantity cannot be negative"):
        Product(
            id=None,
            name="Interior Paint",
            description=None,
            sku="PAINT-001",
            price=850.0,
            quantity=-1,
            created_at="2026-09-12T19:00:00",
        )


def test_product_created_at_cannot_be_empty():
    with pytest.raises(
        ValueError,
        match="Product creation timestamp cannot be empty",
    ):
        Product(
            id=None,
            name="Interior Paint",
            description=None,
            sku="PAINT-001",
            price=850.0,
            quantity=25,
            created_at="",
        )
