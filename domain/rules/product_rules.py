def validate_product_name(name: str) -> None:
    if not name.strip():
        raise ValueError("Product name cannot be empty.")


def validate_product_sku(sku: str) -> None:
    if not sku.strip():
        raise ValueError("Product SKU cannot be empty.")


def validate_product_price(price: float) -> None:
    if price < 0:
        raise ValueError("Product price cannot be negative.")


def validate_product_quantity(quantity: int) -> None:
    if quantity < 0:
        raise ValueError("Product quantity cannot be negative.")


def validate_product_created_at(created_at: str) -> None:
    if not created_at.strip():
        raise ValueError("Product creation timestamp cannot be empty.")