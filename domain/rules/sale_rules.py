def validate_sale_line_product_id(product_id: int) -> None:
    if product_id <= 0:
        raise ValueError("Sale line product ID must be greater than zero")


def validate_sale_line_quantity(quantity: int) -> None:
    if quantity <= 0:
        raise ValueError("Sale line quantity must be greater than zero")


def validate_sale_line_unit_price(unit_price: float) -> None:
    if unit_price < 0:
        raise ValueError("Sale line unit price cannot be negative")
