def validate_sale_line_product_id(product_id: int) -> None:
    if product_id <= 0:
        raise ValueError("Sale line product ID must be greater than zero")


def validate_sale_line_quantity(quantity: int) -> None:
    if quantity <= 0:
        raise ValueError("Sale line quantity must be greater than zero")


def validate_sale_line_unit_price(unit_price: float) -> None:
    if unit_price < 0:
        raise ValueError("Sale line unit price cannot be negative")


def validate_sale_customer_id(customer_id: int) -> None:
    if customer_id <= 0:
        raise ValueError("Sale customer ID must be greater than zero")


def validate_sale_created_at(created_at: str) -> None:
    if not created_at or not created_at.strip():
        raise ValueError("Sale created_at cannot be empty")


def validate_sale_date(sale_date: str) -> None:
    if not sale_date or not sale_date.strip():
        raise ValueError("Sale date cannot be empty")


def validate_sale_total_amount(total_amount: float) -> None:
    if total_amount < 0:
        raise ValueError("Sale total amount cannot be negative")
