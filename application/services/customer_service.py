from domain.entities.customer import Customer
from infrastructure.repositories.customer_repository import CustomerRepository


class CustomerService:
    """Application service for Customer operations."""

    def __init__(self, repository: CustomerRepository) -> None:
        self.repository = repository

    def add_customer(self, customer: Customer) -> None:
        self.repository.add(customer)

    def get_customer(self, customer_id: int) -> Customer | None:
        return self.repository.get_by_id(customer_id)

    def get_customers(self) -> list[Customer]:
        return self.repository.get_all()

    def delete_customer(self, customer_id: int) -> None:
        self.repository.delete(customer_id)
