from domain.entities.product import Product
from application.services.product_service import ProductService


class FakeProductRepository:
    def __init__(self):
        self.added_product = None
        self.products = []
        self.deleted_product_id = None

    def add(self, product):
        self.added_product = product

    def get_by_id(self, product_id):
        for product in self.products:
            if product.id == product_id:
                return product
        return None

    def get_all(self):
        return self.products

    def delete(self, product_id):
        self.deleted_product_id = product_id


def create_product() -> Product:
    return Product(
        id=1,
        name="Interior Paint",
        description="White wall paint",
        sku="PAINT-001",
        price=850.0,
        quantity=25,
        created_at="2026-09-13T10:00:00",
    )


def test_add_product_delegates_to_repository():
    repository = FakeProductRepository()
    service = ProductService(repository)
    product = create_product()

    service.add_product(product)

    assert repository.added_product == product


def test_get_product_delegates_to_repository():
    repository = FakeProductRepository()
    product = create_product()
    repository.products = [product]
    service = ProductService(repository)

    result = service.get_product(product.id)

    assert result == product


def test_get_products_delegates_to_repository():
    repository = FakeProductRepository()
    products = [create_product()]
    repository.products = products
    service = ProductService(repository)

    result = service.get_products()

    assert result == products


def test_delete_product_delegates_to_repository():
    repository = FakeProductRepository()
    service = ProductService(repository)

    service.delete_product(1)

    assert repository.deleted_product_id == 1
