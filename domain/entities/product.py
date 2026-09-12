from dataclasses import dataclass

from domain.rules.product_rules import (
    validate_product_created_at,
    validate_product_name,
    validate_product_price,
    validate_product_quantity,
    validate_product_sku,
)


@dataclass
class Product:
    id: int | None
    name: str
    description: str | None
    sku: str
    price: float
    quantity: int
    created_at: str

    def __post_init__(self) -> None:
        validate_product_name(self.name)
        validate_product_sku(self.sku)
        validate_product_price(self.price)
        validate_product_quantity(self.quantity)
        validate_product_created_at(self.created_at)
