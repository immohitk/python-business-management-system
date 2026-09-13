from domain.entities.customer import Customer
from application.services.customer_service import CustomerService


class FakeCustomerRepository:
    def __init__(self):
        self.added_customer = None
        self.customers = []
        self.deleted_customer_id = None

    def add(self, customer):
        self.added_customer = customer

    def get_by_id(self, customer_id):
        for customer in self.customers:
            if customer.id == customer_id:
                return customer
        return None

    def get_all(self):
        return self.customers

    def delete(self, customer_id):
        self.deleted_customer_id = customer_id


def create_customer() -> Customer:
    return Customer(
        id=1,
        name="Rahul Sharma",
        phone="9876543210",
        email="rahul@example.com",
        address="Delhi",
        created_at="2026-09-13T10:00:00",
    )


def test_add_customer_delegates_to_repository():
    repository = FakeCustomerRepository()
    service = CustomerService(repository)
    customer = create_customer()

    service.add_customer(customer)

    assert repository.added_customer == customer


def test_get_customer_delegates_to_repository():
    repository = FakeCustomerRepository()
    customer = create_customer()
    repository.customers = [customer]
    service = CustomerService(repository)

    result = service.get_customer(customer.id)

    assert result == customer


def test_get_customers_delegates_to_repository():
    repository = FakeCustomerRepository()
    customers = [create_customer()]
    repository.customers = customers
    service = CustomerService(repository)

    result = service.get_customers()

    assert result == customers


def test_delete_customer_delegates_to_repository():
    repository = FakeCustomerRepository()
    service = CustomerService(repository)

    service.delete_customer(1)

    assert repository.deleted_customer_id == 1
