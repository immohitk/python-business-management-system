from dataclasses import dataclass

from domain.rules.sale_payment_rules import (
    validate_sale_payment_amount,
    validate_sale_payment_created_at,
    validate_sale_payment_mode,
    validate_sale_payment_sale_id,
)


@dataclass
class SalePayment:
    id: int | None
    sale_id: int
    payment_mode: str
    amount: float
    created_at: str

    def __post_init__(self) -> None:
        validate_sale_payment_sale_id(self.sale_id)
        validate_sale_payment_mode(self.payment_mode)
        validate_sale_payment_amount(self.amount)
        validate_sale_payment_created_at(self.created_at)
