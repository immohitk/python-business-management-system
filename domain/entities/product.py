from dataclasses import dataclass, field

from domain.entities.stock_movement import (
    StockMovement,
    StockMovementType,
)

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
    validate_product_unit,
    validate_conversion_factor,
    validate_margin,
    validate_margin_range,
    validate_mrp,
    validate_default_tax_id,
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
    category_id: int | None = None
    base_unit: str = "PCS"
    purchase_unit: str = "PCS"
    sales_unit: str = "PCS"
    purchase_to_base_conversion: float = 1.0
    sales_to_base_conversion: float = 1.0
    is_perishable: bool = False
    mrp_applicable: bool = False
    default_mrp: float | None = None
    default_margin: float = 0.0
    min_margin: float = 0.0
    max_margin: float = 100.0
    default_tax_id: int | None = None

    movements: list[StockMovement] = field(default_factory=list)

    def __post_init__(self) -> None:
        validate_product_name(self.name)
        validate_product_sku(self.sku)
        validate_product_price(self.price)
        validate_product_quantity(self.quantity)
        validate_product_created_at(self.created_at)
        validate_product_unit(self.base_unit, "base")
        validate_product_unit(self.purchase_unit, "purchase")
        validate_product_unit(self.sales_unit, "sales")
        validate_conversion_factor(self.purchase_to_base_conversion, "purchase-to-base")
        validate_conversion_factor(self.sales_to_base_conversion, "sales-to-base")
        validate_margin(self.default_margin, "default")
        validate_margin(self.min_margin, "minimum")
        validate_margin(self.max_margin, "maximum")
        validate_margin_range(self.default_margin, self.min_margin, self.max_margin)
        validate_mrp(self.mrp_applicable, self.default_mrp)
        validate_default_tax_id(self.default_tax_id)

    def add_stock(self, amount: int, created_at: str) -> None:
        validate_stock_addition(amount)

        self.quantity += amount
        validate_stock_quantity(self.quantity)

        self.movements.append(
            StockMovement(
                movement_type=StockMovementType.ADD,
                quantity=amount,
                resulting_stock=self.quantity,
                created_at=created_at,
            )
        )

    def adjust_stock(self, quantity: int, created_at: str) -> None:
        validate_stock_adjustment(quantity)

        self.quantity = quantity

        self.movements.append(
            StockMovement(
                movement_type=StockMovementType.ADJUST,
                quantity=quantity,
                resulting_stock=self.quantity,
                created_at=created_at,
            )
        )

    def deduct_stock(self, amount: int, created_at: str) -> None:
        validate_stock_deduction(amount)

        new_quantity = self.quantity - amount
        validate_stock_quantity(new_quantity)

        self.quantity = new_quantity

        self.movements.append(
            StockMovement(
                movement_type=StockMovementType.DEDUCT,
                quantity=amount,
                resulting_stock=self.quantity,
                created_at=created_at,
            )
        )
