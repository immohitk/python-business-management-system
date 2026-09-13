from domain.entities.supplier import Supplier

from application.services.supplier_service import SupplierService


class FakeSupplierRepository:
    def __init__(self):
        self.added_supplier = None
        self.suppliers = []
        self.deleted_supplier_id = None

    def add(self, supplier):
        self.added_supplier = supplier

    def get_by_id(self, supplier_id):
        for supplier in self.suppliers:
            if supplier.id == supplier_id:
                return supplier
        return None

    def get_all(self):
        return self.suppliers

    def delete(self, supplier_id):
        self.deleted_supplier_id = supplier_id


def create_supplier() -> Supplier:
    return Supplier(
        id=1,
        name="ABC Suppliers",
        phone="9876543210",
        email="abc@example.com",
        address="Delhi",
        created_at="2026-09-13T10:00:00",
    )


def test_add_supplier_delegates_to_repository():
    repository = FakeSupplierRepository()
    service = SupplierService(repository)
    supplier = create_supplier()

    service.add_supplier(supplier)

    assert repository.added_supplier == supplier


def test_get_supplier_delegates_to_repository():
    repository = FakeSupplierRepository()
    supplier = create_supplier()
    repository.suppliers = [supplier]
    service = SupplierService(repository)

    result = service.get_supplier(supplier.id)

    assert result == supplier


def test_get_suppliers_delegates_to_repository():
    repository = FakeSupplierRepository()
    suppliers = [create_supplier()]
    repository.suppliers = suppliers
    service = SupplierService(repository)

    result = service.get_suppliers()

    assert result == suppliers


def test_delete_supplier_delegates_to_repository():
    repository = FakeSupplierRepository()
    service = SupplierService(repository)

    service.delete_supplier(1)

    assert repository.deleted_supplier_id == 1
