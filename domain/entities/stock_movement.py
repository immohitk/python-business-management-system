from dataclasses import dataclass
from enum import Enum

from domain.rules.inventory_rules import validate_stock_quantity


class StockMovementType(Enum):
    ADD = "ADD"
    ADJUST = "ADJUST"
    DEDUCT = "DEDUCT"


@dataclass(frozen=True)
class StockMovement:
    movement_type: StockMovementType
    quantity: int
    resulting_stock: int

    def __post_init__(self) -> None:
        validate_stock_quantity(self.quantity)
        validate_stock_quantity(self.resulting_stock)
