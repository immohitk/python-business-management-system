def validate_invoice_sale_id(sale_id: int) -> None:
    if sale_id <= 0:
        raise ValueError("Invoice sale ID must be greater than zero")


def validate_invoice_date(invoice_date: str) -> None:
    if not invoice_date or not invoice_date.strip():
        raise ValueError("Invoice date cannot be empty")


def validate_invoice_total_amount(total_amount: float) -> None:
    if total_amount < 0:
        raise ValueError("Invoice total amount cannot be negative")


def validate_invoice_created_at(created_at: str) -> None:
    if not created_at or not created_at.strip():
        raise ValueError("Invoice created_at cannot be empty")


def validate_invoice_number(invoice_number: str) -> None:
    if not invoice_number or not invoice_number.strip():
        raise ValueError("Invoice number cannot be empty")
