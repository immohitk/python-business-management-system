from domain.entities.product import Product
from infrastructure.repositories.product_repository import ProductRepository
from infrastructure.repositories.stock_movement_repository import (
    StockMovementRepository,
)


class InventoryService:
    """Application service for inventory operations."""

    def __init__(
        self,
        product_repository: ProductRepository,
        stock_movement_repository: StockMovementRepository,
    ) -> None:
        self.product_repository = product_repository
        self.stock_movement_repository = stock_movement_repository

    def stock_in(self, product_id: int, amount: int) -> None:
        product = self.product_repository.get_by_id(product_id)

        if product is None:
            raise ValueError("Product not found.")

        product.add_stock(amount)

        self.product_repository.update(product)

        movement = product.movements[-1]
        self.stock_movement_repository.add_movement(
            product_id,
            movement,
        )

    def adjust_stock(self, product_id: int, quantity: int) -> None:
        product = self.product_repository.get_by_id(product_id)

        if product is None:
            raise ValueError("Product not found.")

        product.adjust_stock(quantity)

        self.product_repository.update(product)

        movement = product.movements[-1]
        self.stock_movement_repository.add_movement(
            product_id,
            movement,
        )
