from pathlib import Path

from domain.entities.customer import Customer
from infrastructure.database.connection import get_connection
from infrastructure.database.initialization import initialize_database
from infrastructure.repositories.customer_repository import CustomerRepository


def create_repository(tmp_path: Path) -> tuple[CustomerRepository, object]:
    database_path = tmp_path / "test.db"
    initialize_database(database_path)
    connection = get_connection(database_path)

    return CustomerRepository(connection), connection


def create_customer() -> Customer:
    return Customer(
        id=None,
        name="Rahul Sharma",
        phone="9876543210",
        email="rahul@example.com",
        address="Delhi",
        created_at="2026-09-07T20:00:00",
    )


def test_add_customer(tmp_path):
    repository, connection = create_repository(tmp_path)

    try:
        customer = create_customer()

        repository.add(customer)

        assert customer.id is not None
        assert customer.id > 0
    finally:
        connection.close()


def test_get_customer_by_id(tmp_path):
    repository, connection = create_repository(tmp_path)

    try:
        customer = create_customer()
        repository.add(customer)

        result = repository.get_by_id(customer.id)

        assert result == customer
    finally:
        connection.close()


def test_get_customer_by_id_returns_none_for_missing_customer(tmp_path):
    repository, connection = create_repository(tmp_path)

    try:
        result = repository.get_by_id(999)

        assert result is None
    finally:
        connection.close()


def test_get_all_customers(tmp_path):
    repository, connection = create_repository(tmp_path)

    try:
        first_customer = create_customer()
        second_customer = Customer(
            id=None,
            name="Priya Verma",
            phone="9123456780",
            email="priya@example.com",
            address="Mumbai",
            created_at="2026-09-07T20:00:00",
        )

        repository.add(first_customer)
        repository.add(second_customer)

        result = repository.get_all()

        assert result == [first_customer, second_customer]
    finally:
        connection.close()


def test_delete_customer(tmp_path):
    repository, connection = create_repository(tmp_path)

    try:
        customer = create_customer()
        repository.add(customer)

        repository.delete(customer.id)

        assert repository.get_by_id(customer.id) is None
    finally:
        connection.close()