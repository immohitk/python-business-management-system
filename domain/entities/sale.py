from dataclasses import dataclass, field

from domain.entities.sale_line import SaleLine
from domain.rules.sale_rules import (
    validate_sale_created_at,
    validate_sale_customer_id,
    validate_sale_date,
    validate_sale_total_amount,
)


@dataclass
class Sale:
    id: int | None
    customer_id: int
    sale_date: str
    total_amount: float
    created_at: str
    lines: list[SaleLine] = field(default_factory=list)

    def __post_init__(self) -> None:
        validate_sale_customer_id(self.customer_id)
        validate_sale_date(self.sale_date)
        validate_sale_total_amount(self.total_amount)
        validate_sale_created_at(self.created_at)

    @property
    def calculated_total(self) -> float:
        return sum(line.subtotal for line in self.lines)
