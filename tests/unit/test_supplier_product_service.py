from application.services.supplier_product_service import SupplierProductService


class FakeSupplierProductRepository:
    def __init__(self):
        self.assignments = set()

    def add(self, supplier_id, product_id):
        self.assignments.add((supplier_id, product_id))

    def remove(self, supplier_id, product_id):
        self.assignments.discard((supplier_id, product_id))

    def get_product_ids_for_supplier(self, supplier_id):
        return sorted(product_id for sid, product_id in self.assignments if sid == supplier_id)

    def get_supplier_ids_for_product(self, product_id):
        return sorted(supplier_id for supplier_id, pid in self.assignments if pid == product_id)

    def exists(self, supplier_id, product_id):
        return (supplier_id, product_id) in self.assignments


def test_assign_supplier_to_product():
    repository = FakeSupplierProductRepository()
    service = SupplierProductService(repository)

    service.assign_supplier_to_product(1, 10)

    assert service.get_suppliers_for_product(10) == [1]


def test_remove_supplier_from_product():
    repository = FakeSupplierProductRepository()
    service = SupplierProductService(repository)
    service.assign_supplier_to_product(1, 10)

    service.remove_supplier_from_product(1, 10)

    assert service.get_suppliers_for_product(10) == []


def test_product_can_have_multiple_suppliers():
    repository = FakeSupplierProductRepository()
    service = SupplierProductService(repository)
    service.assign_supplier_to_product(1, 10)
    service.assign_supplier_to_product(2, 10)

    assert service.get_suppliers_for_product(10) == [1, 2]


def test_supplier_can_have_multiple_products():
    repository = FakeSupplierProductRepository()
    service = SupplierProductService(repository)
    service.assign_supplier_to_product(1, 10)
    service.assign_supplier_to_product(1, 11)

    assert service.get_products_for_supplier(1) == [10, 11]
