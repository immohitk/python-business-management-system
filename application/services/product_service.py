from domain.entities.product import Product
from infrastructure.repositories.product_repository import ProductRepository


class ProductService:
    def __init__(self, repository: ProductRepository):
        self.repository = repository

    def add_product(self, product: Product) -> None:
        self.repository.add(product)

    def get_product(self, product_id: int):
        return self.repository.get_by_id(product_id)

    def get_products(self):
        return self.repository.get_all()

    def update_product(self, product: Product) -> None:
        self.repository.update(product)

    def delete_product(self, product_id: int) -> None:
        self.repository.delete(product_id)

    def get_edit_history(self, product_id: int):
        return self.repository.get_edit_history(product_id)

    def get_product_history(self):
        return self.repository.get_product_history()
