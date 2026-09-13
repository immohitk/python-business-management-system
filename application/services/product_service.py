from domain.entities.product import Product
from infrastructure.repositories.product_repository import ProductRepository


class ProductService:
    """Application service for Product operations."""

    def __init__(self, repository: ProductRepository) -> None:
        self.repository = repository

    def add_product(self, product: Product) -> None:
        self.repository.add(product)

    def get_product(self, product_id: int) -> Product | None:
        return self.repository.get_by_id(product_id)

    def get_products(self) -> list[Product]:
        return self.repository.get_all()

    def delete_product(self, product_id: int) -> None:
        self.repository.delete(product_id)
