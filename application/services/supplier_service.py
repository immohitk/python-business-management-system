from domain.entities.supplier import Supplier
from infrastructure.repositories.supplier_repository import SupplierRepository


class SupplierService:
    """Application service for Supplier operations."""

    def __init__(self, repository: SupplierRepository) -> None:
        self.repository = repository

    def add_supplier(self, supplier: Supplier) -> None:
        self.repository.add(supplier)

    def get_supplier(self, supplier_id: int) -> Supplier | None:
        return self.repository.get_by_id(supplier_id)

    def get_suppliers(self) -> list[Supplier]:
        return self.repository.get_all()

    def delete_supplier(self, supplier_id: int) -> None:
        self.repository.delete(supplier_id)
