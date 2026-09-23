from dataclasses import dataclass

from domain.rules.invoice_rules import (
    validate_invoice_created_at,
    validate_invoice_date,
    validate_invoice_sale_id,
    validate_invoice_total_amount,
)


@dataclass
class Invoice:
    id: int | None
    sale_id: int
    invoice_number: str
    invoice_date: str
    total_amount: float
    created_at: str

    def __post_init__(self) -> None:
        validate_invoice_sale_id(self.sale_id)
        validate_invoice_date(self.invoice_date)
        validate_invoice_total_amount(self.total_amount)
        validate_invoice_created_at(self.created_at)
