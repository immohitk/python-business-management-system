def validate_stock_quantity(quantity: int) -> None:
    if quantity < 0:
        raise ValueError("Stock quantity cannot be negative.")


def validate_stock_addition(amount: int) -> None:
    if amount <= 0:
        raise ValueError("Stock addition amount must be greater than zero.")


def validate_stock_adjustment(quantity: int) -> None:
    validate_stock_quantity(quantity)


def validate_stock_deduction(amount: int) -> None:
    if amount <= 0:
        raise ValueError("Stock deduction amount must be greater than zero.")
