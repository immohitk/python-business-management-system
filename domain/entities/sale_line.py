from dataclasses import dataclass

from domain.rules.sale_rules import (
    validate_sale_line_product_id,
    validate_sale_line_quantity,
    validate_sale_line_unit_price,
)


@dataclass
class SaleLine:
    product_id: int
    quantity: int
    unit_price: float

    def __post_init__(self) -> None:
        validate_sale_line_product_id(self.product_id)
        validate_sale_line_quantity(self.quantity)
        validate_sale_line_unit_price(self.unit_price)

    @property
    def subtotal(self) -> float:
        return self.quantity * self.unit_price
