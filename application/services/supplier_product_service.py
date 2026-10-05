from infrastructure.repositories.supplier_product_repository import (
    SupplierProductRepository,
)


class SupplierProductService:
    """Application service for the many-to-many Supplier ↔ Product relationship."""

    def __init__(self, repository: SupplierProductRepository) -> None:
        self.repository = repository

    def assign_supplier_to_product(self, supplier_id: int, product_id: int) -> None:
        self.repository.add(supplier_id, product_id)

    def remove_supplier_from_product(self, supplier_id: int, product_id: int) -> None:
        self.repository.remove(supplier_id, product_id)

    def get_products_for_supplier(self, supplier_id: int) -> list[int]:
        return self.repository.get_product_ids_for_supplier(supplier_id)

    def get_suppliers_for_product(self, product_id: int) -> list[int]:
        return self.repository.get_supplier_ids_for_product(product_id)

    def supplier_supplies_product(self, supplier_id: int, product_id: int) -> bool:
        return self.repository.exists(supplier_id, product_id)
