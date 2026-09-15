from dataclasses import dataclass

from domain.rules.inventory_rules import (
    validate_stock_addition,
    validate_stock_adjustment,
    validate_stock_deduction,
    validate_stock_quantity,
)
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

    def add_stock(self, amount: int) -> None:
        validate_stock_addition(amount)
        self.quantity += amount
        validate_stock_quantity(self.quantity)

    def adjust_stock(self, quantity: int) -> None:
        validate_stock_adjustment(quantity)
        self.quantity = quantity

    def deduct_stock(self, amount: int) -> None:
        validate_stock_deduction(amount)

        new_quantity = self.quantity - amount
        validate_stock_quantity(new_quantity)

        self.quantity = new_quantity
