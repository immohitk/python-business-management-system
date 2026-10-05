import pytest

from domain.entities.product import Product

from domain.entities.stock_movement import StockMovementType


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


def test_product_allows_zero_price():
    product = Product(
        id=None,
        name="Free Sample",
        description=None,
        sku="SAMPLE-001",
        price=0,
        quantity=10,
        created_at="2026-09-12T19:00:00",
    )

    assert product.price == 0


def test_product_allows_zero_quantity():
    product = Product(
        id=None,
        name="Out of Stock Paint",
        description=None,
        sku="PAINT-OUT-001",
        price=850.0,
        quantity=0,
        created_at="2026-09-12T19:00:00",
    )

    assert product.quantity == 0


def test_product_name_cannot_contain_only_whitespace():
    with pytest.raises(ValueError, match="Product name cannot be empty"):
        Product(
            id=None,
            name="   ",
            description=None,
            sku="PAINT-001",
            price=850.0,
            quantity=10,
            created_at="2026-09-12T19:00:00",
        )


def test_product_sku_cannot_contain_only_whitespace():
    with pytest.raises(ValueError, match="Product SKU cannot be empty"):
        Product(
            id=None,
            name="Interior Paint",
            description=None,
            sku="   ",
            price=850.0,
            quantity=10,
            created_at="2026-09-12T19:00:00",
        )


def test_product_allows_optional_description():
    product = Product(
        id=None,
        name="Interior Paint",
        description=None,
        sku="PAINT-002",
        price=850.0,
        quantity=10,
        created_at="2026-09-12T19:00:00",
    )

    assert product.description is None


def test_product_allows_none_id_before_persistence():
    product = Product(
        id=None,
        name="Interior Paint",
        description="White wall paint",
        sku="PAINT-003",
        price=850.0,
        quantity=10,
        created_at="2026-09-12T19:00:00",
    )

    assert product.id is None


def test_product_add_stock():
    product = Product(
        id=1,
        name="Laptop",
        description="Business laptop",
        sku="LAP-001",
        price=50000.0,
        quantity=10,
        created_at="2026-01-01T10:00:00",
    )

    product.add_stock(5, "2026-09-17T10:00:00")

    assert product.quantity == 15


def test_product_adjust_stock():
    product = Product(
        id=1,
        name="Laptop",
        description="Business laptop",
        sku="LAP-001",
        price=50000.0,
        quantity=10,
        created_at="2026-01-01T10:00:00",
    )

    product.adjust_stock(7, "2026-09-17T10:00:00")

    assert product.quantity == 7


def test_product_deduct_stock():
    product = Product(
        id=1,
        name="Laptop",
        description="Business laptop",
        sku="LAP-001",
        price=50000.0,
        quantity=10,
        created_at="2026-01-01T10:00:00",
    )

    product.deduct_stock(3, "2026-09-17T10:00:00")

    assert product.quantity == 7


def test_product_add_stock_rejects_zero():
    product = Product(
        id=1,
        name="Laptop",
        description="Business laptop",
        sku="LAP-001",
        price=50000.0,
        quantity=10,
        created_at="2026-01-01T10:00:00",
    )

    with pytest.raises(
        ValueError,
        match="Stock addition amount must be greater than zero",
    ):
        product.add_stock(0, "2026-09-17T10:00:00")

    assert product.quantity == 10


def test_product_adjust_stock_rejects_negative_quantity():
    product = Product(
        id=1,
        name="Laptop",
        description="Business laptop",
        sku="LAP-001",
        price=50000.0,
        quantity=10,
        created_at="2026-01-01T10:00:00",
    )

    with pytest.raises(
        ValueError,
        match="Stock quantity cannot be negative",
    ):
        product.adjust_stock(-1, "2026-09-17T10:00:00")

    assert product.quantity == 10


def test_product_deduct_stock_rejects_zero():
    product = Product(
        id=1,
        name="Laptop",
        description="Business laptop",
        sku="LAP-001",
        price=50000.0,
        quantity=10,
        created_at="2026-01-01T10:00:00",
    )

    with pytest.raises(
        ValueError,
        match="Stock deduction amount must be greater than zero",
    ):
        product.deduct_stock(0, "2026-09-17T10:00:00")

    assert product.quantity == 10


def test_product_deduct_stock_rejects_amount_greater_than_stock():
    product = Product(
        id=1,
        name="Laptop",
        description="Business laptop",
        sku="LAP-001",
        price=50000.0,
        quantity=10,
        created_at="2026-01-01T10:00:00",
    )

    with pytest.raises(
        ValueError,
        match="Stock quantity cannot be negative",
    ):
        product.deduct_stock(11, "2026-09-17T10:00:00")

    assert product.quantity == 10


def test_product_deduct_stock_allows_exact_available_stock():
    product = Product(
        id=1,
        name="Laptop",
        description="Business laptop",
        sku="LAP-001",
        price=50000.0,
        quantity=10,
        created_at="2026-01-01T10:00:00",
    )

    product.deduct_stock(10, "2026-09-17T10:00:00")

    assert product.quantity == 0


def test_product_adjust_stock_allows_zero():
    product = Product(
        id=1,
        name="Laptop",
        description="Business laptop",
        sku="LAP-001",
        price=50000.0,
        quantity=10,
        created_at="2026-01-01T10:00:00",
    )

    product.adjust_stock(0, "2026-09-17T10:00:00")

    assert product.quantity == 0


def test_product_add_stock_from_zero():
    product = Product(
        id=1,
        name="Laptop",
        description="Business laptop",
        sku="LAP-001",
        price=50000.0,
        quantity=0,
        created_at="2026-01-01T10:00:00",
    )

    product.add_stock(5, "2026-09-17T10:00:00")

    assert product.quantity == 5


def test_product_add_stock_records_movement():
    product = Product(
        id=1,
        name="Laptop",
        description="Business laptop",
        sku="LAP-001",
        price=50000.0,
        quantity=10,
        created_at="2026-01-01T10:00:00",
    )

    product.add_stock(5, "2026-09-17T10:00:00")

    assert len(product.movements) == 1
    assert product.movements[0].movement_type == StockMovementType.ADD
    assert product.movements[0].quantity == 5
    assert product.movements[0].resulting_stock == 15
    assert product.movements[0].created_at == "2026-09-17T10:00:00"


def test_product_adjust_stock_records_movement():
    product = Product(
        id=1,
        name="Laptop",
        description="Business laptop",
        sku="LAP-001",
        price=50000.0,
        quantity=10,
        created_at="2026-01-01T10:00:00",
    )

    product.adjust_stock(7, "2026-09-17T10:00:00")

    assert len(product.movements) == 1
    assert product.movements[0].movement_type == StockMovementType.ADJUST
    assert product.movements[0].quantity == 7
    assert product.movements[0].resulting_stock == 7
    assert product.movements[0].created_at == "2026-09-17T10:00:00"


def test_product_deduct_stock_records_movement():
    product = Product(
        id=1,
        name="Laptop",
        description="Business laptop",
        sku="LAP-001",
        price=50000.0,
        quantity=10,
        created_at="2026-01-01T10:00:00",
    )

    product.deduct_stock(3, "2026-09-17T10:00:00")

    assert len(product.movements) == 1
    assert product.movements[0].movement_type == StockMovementType.DEDUCT
    assert product.movements[0].quantity == 3
    assert product.movements[0].resulting_stock == 7
    assert product.movements[0].created_at == "2026-09-17T10:00:00"


def test_product_failed_add_stock_does_not_record_movement():
    product = Product(
        id=1,
        name="Laptop",
        description="Business laptop",
        sku="LAP-001",
        price=50000.0,
        quantity=10,
        created_at="2026-01-01T10:00:00",
    )

    with pytest.raises(
        ValueError,
        match="Stock addition amount must be greater than zero",
    ):
        product.add_stock(0, "2026-09-17T10:00:00")

    assert product.quantity == 10
    assert product.movements == []


def test_product_failed_adjust_stock_does_not_record_movement():
    product = Product(
        id=1,
        name="Laptop",
        description="Business laptop",
        sku="LAP-001",
        price=50000.0,
        quantity=10,
        created_at="2026-01-01T10:00:00",
    )

    with pytest.raises(
        ValueError,
        match="Stock quantity cannot be negative",
    ):
        product.adjust_stock(-1, "2026-09-17T10:00:00")

    assert product.quantity == 10
    assert product.movements == []


def test_product_failed_deduct_stock_does_not_record_movement():
    product = Product(
        id=1,
        name="Laptop",
        description="Business laptop",
        sku="LAP-001",
        price=50000.0,
        quantity=10,
        created_at="2026-01-01T10:00:00",
    )

    with pytest.raises(
        ValueError,
        match="Stock quantity cannot be negative",
    ):
        product.deduct_stock(11, "2026-09-17T10:00:00")

    assert product.quantity == 10
    assert product.movements == []


def test_product_supports_v2_business_defaults():
    product = Product(
        id=None,
        name="Rice",
        description="Premium rice",
        sku="RICE-001",
        price=120.0,
        quantity=10,
        created_at="2026-10-05T10:00:00",
        category_id=2,
        base_unit="KG",
        purchase_unit="BAG",
        sales_unit="KG",
        purchase_to_base_conversion=25.0,
        sales_to_base_conversion=1.0,
        is_perishable=True,
        mrp_applicable=True,
        default_mrp=150.0,
        default_margin=20.0,
        min_margin=10.0,
        max_margin=30.0,
        default_tax_id=3,
    )

    assert product.category_id == 2
    assert product.base_unit == "KG"
    assert product.purchase_unit == "BAG"
    assert product.sales_unit == "KG"
    assert product.purchase_to_base_conversion == 25.0
    assert product.is_perishable is True
    assert product.mrp_applicable is True
    assert product.default_mrp == 150.0
    assert product.default_margin == 20.0
    assert product.default_tax_id == 3


def test_product_rejects_invalid_margin_range():
    with pytest.raises(ValueError, match="minimum margin cannot exceed maximum"):
        Product(
            id=None,
            name="Rice",
            description=None,
            sku="RICE-002",
            price=120.0,
            quantity=1,
            created_at="2026-10-05T10:00:00",
            default_margin=20.0,
            min_margin=40.0,
            max_margin=30.0,
        )


def test_product_requires_mrp_when_applicable():
    with pytest.raises(ValueError, match="Default MRP is required"):
        Product(
            id=None,
            name="Rice",
            description=None,
            sku="RICE-003",
            price=120.0,
            quantity=1,
            created_at="2026-10-05T10:00:00",
            mrp_applicable=True,
        )
