from domain.entities.supplier import Supplier
from presentation.cli.suppliers import (
    add_supplier,
    delete_supplier,
    get_supplier,
    list_suppliers,
)


class FakeSupplierService:
    def __init__(self):
        self.added_supplier = None

    def add_supplier(self, supplier):
        supplier.id = 1
        self.added_supplier = supplier


def test_add_supplier_creates_and_persists_supplier(monkeypatch, capsys):
    service = FakeSupplierService()

    inputs = iter(
        [
            "ABC Suppliers",
            "9123456780",
            "supplier@example.com",
            "Mumbai",
        ]
    )

    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    add_supplier(service)

    captured = capsys.readouterr()

    assert service.added_supplier is not None
    assert service.added_supplier.name == "ABC Suppliers"
    assert service.added_supplier.phone == "9123456780"
    assert service.added_supplier.email == "supplier@example.com"
    assert service.added_supplier.address == "Mumbai"
    assert service.added_supplier.id == 1
    assert "Supplier added successfully with ID: 1" in captured.out


def test_list_suppliers_displays_suppliers(capsys):
    supplier = Supplier(
        id=1,
        name="ABC Suppliers",
        phone="9123456780",
        email="supplier@example.com",
        address="Mumbai",
        created_at="2026-08-09T10:00:00",
    )

    class FakeSupplierService:
        def get_suppliers(self):
            return [supplier]

    service = FakeSupplierService()

    list_suppliers(service)

    captured = capsys.readouterr()

    assert "Supplier List" in captured.out
    assert "ID: 1" in captured.out
    assert "Name: ABC Suppliers" in captured.out
    assert "Phone: 9123456780" in captured.out
    assert "Email: supplier@example.com" in captured.out


def test_get_supplier_displays_supplier(capsys, monkeypatch):
    supplier = Supplier(
        id=1,
        name="ABC Suppliers",
        phone="9123456780",
        email="supplier@example.com",
        address="Mumbai",
        created_at="2026-08-09T10:00:00",
    )

    class FakeSupplierService:
        def get_supplier(self, supplier_id):
            assert supplier_id == 1
            return supplier

    monkeypatch.setattr("builtins.input", lambda _: "1")

    service = FakeSupplierService()

    get_supplier(service)

    captured = capsys.readouterr()

    assert "Get Supplier" in captured.out
    assert "ID: 1" in captured.out
    assert "Name: ABC Suppliers" in captured.out
    assert "Phone: 9123456780" in captured.out
    assert "Email: supplier@example.com" in captured.out
    assert "Address: Mumbai" in captured.out


def test_delete_supplier_deletes_supplier(capsys, monkeypatch):
    class FakeSupplierService:
        def delete_supplier(self, supplier_id):
            assert supplier_id == 1

    monkeypatch.setattr("builtins.input", lambda _: "1")

    service = FakeSupplierService()
    delete_supplier(service)

    captured = capsys.readouterr()

    assert "Delete Supplier" in captured.out
    assert "Supplier deleted successfully with ID: 1" in captured.out
