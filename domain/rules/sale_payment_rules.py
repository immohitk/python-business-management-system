PAYMENT_MODES = {
    "Cash",
    "UPI",
    "Card",
    "Bank Transfer",
    "Other",
}


def validate_sale_payment_sale_id(sale_id: int) -> None:
    if sale_id <= 0:
        raise ValueError("Sale ID must be greater than zero.")


def validate_sale_payment_mode(payment_mode: str) -> None:
    if payment_mode not in PAYMENT_MODES:
        raise ValueError(
            "Payment mode must be Cash, UPI, Card, Bank Transfer, or Other."
        )


def validate_sale_payment_amount(amount: float) -> None:
    if amount <= 0:
        raise ValueError("Payment amount must be greater than zero.")


def validate_sale_payment_created_at(created_at: str) -> None:
    if not created_at.strip():
        raise ValueError("Payment creation timestamp cannot be empty.")