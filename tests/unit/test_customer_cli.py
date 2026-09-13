from domain.entities.customer import Customer
from presentation.cli.customers import (
    add_customer,
    delete_customer,
    get_customer,
    list_customers,
)


class FakeCustomerService:
    def __init__(self):
        self.added_customer = None

    def add_customer(self, customer):
        customer.id = 1
        self.added_customer = customer


def test_add_customer_creates_and_persists_customer(monkeypatch, capsys):
    service = FakeCustomerService()

    inputs = iter(
        [
            "Rahul Sharma",
            "9876543210",
            "rahul@example.com",
            "Bengaluru",
        ]
    )

    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    add_customer(service)

    captured = capsys.readouterr()

    assert service.added_customer is not None
    assert service.added_customer.name == "Rahul Sharma"
    assert service.added_customer.phone == "9876543210"
    assert service.added_customer.email == "rahul@example.com"
    assert service.added_customer.address == "Bengaluru"
    assert service.added_customer.id == 1
    assert "Customer added successfully with ID: 1" in captured.out


def test_list_customers_displays_customers(capsys):
    customer = Customer(
        id=1,
        name="Rahul Sharma",
        phone="9876543210",
        email="rahul@example.com",
        address="Bengaluru",
        created_at="2026-08-09T10:00:00",
    )

    class FakeCustomerService:
        def get_customers(self):
            return [customer]

    service = FakeCustomerService()

    list_customers(service)

    captured = capsys.readouterr()

    assert "Customer List" in captured.out
    assert "ID: 1" in captured.out
    assert "Name: Rahul Sharma" in captured.out
    assert "Phone: 9876543210" in captured.out
    assert "Email: rahul@example.com" in captured.out


def test_get_customer_displays_customer(capsys, monkeypatch):
    customer = Customer(
        id=1,
        name="Rahul Sharma",
        phone="9876543210",
        email="rahul@example.com",
        address="Bengaluru",
        created_at="2026-08-09T10:00:00",
    )

    class FakeCustomerService:
        def get_customer(self, customer_id):
            assert customer_id == 1
            return customer

    monkeypatch.setattr("builtins.input", lambda _: "1")

    service = FakeCustomerService()

    get_customer(service)

    captured = capsys.readouterr()

    assert "Get Customer" in captured.out
    assert "ID: 1" in captured.out
    assert "Name: Rahul Sharma" in captured.out
    assert "Phone: 9876543210" in captured.out
    assert "Email: rahul@example.com" in captured.out
    assert "Address: Bengaluru" in captured.out


def test_delete_customer_deletes_customer(capsys, monkeypatch):
    class FakeCustomerService:
        def __init__(self):
            self.deleted_customer_id = None

        def delete_customer(self, customer_id):
            self.deleted_customer_id = customer_id

    service = FakeCustomerService()

    monkeypatch.setattr("builtins.input", lambda _: "1")

    delete_customer(service)

    captured = capsys.readouterr()

    assert service.deleted_customer_id == 1
    assert "Delete Customer" in captured.out
    assert "Customer deleted successfully with ID: 1" in captured.out
