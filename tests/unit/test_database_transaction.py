import sqlite3

import pytest

from domain.entities.customer import Customer
from infrastructure.repositories.customer_repository import CustomerRepository
from infrastructure.database.initialization import initialize_database
from infrastructure.database.transaction import transaction


def create_connection() -> sqlite3.Connection:
    connection = sqlite3.connect(":memory:")
    connection.execute(
        """
        CREATE TABLE records (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        )
        """
    )
    return connection


def test_transaction_commits_successful_operations():
    connection = create_connection()

    try:
        with transaction(connection):
            connection.execute(
                "INSERT INTO records (name) VALUES (?)",
                ("first",),
            )
            connection.execute(
                "INSERT INTO records (name) VALUES (?)",
                ("second",),
            )

        rows = connection.execute(
            "SELECT name FROM records ORDER BY id"
        ).fetchall()

        assert rows == [("first",), ("second",)]
    finally:
        connection.close()


def test_transaction_rolls_back_failed_operations():
    connection = create_connection()

    try:
        with pytest.raises(ValueError, match="transaction failed"):
            with transaction(connection):
                connection.execute(
                    "INSERT INTO records (name) VALUES (?)",
                    ("first",),
                )
                raise ValueError("transaction failed")

        rows = connection.execute(
            "SELECT name FROM records"
        ).fetchall()

        assert rows == []
    finally:
        connection.close()


def test_repository_operations_roll_back_inside_transaction(tmp_path):
    database_path = tmp_path / "transaction.db"
    initialize_database(database_path)

    connection = sqlite3.connect(database_path)

    try:
        repository = CustomerRepository(connection)

        customer = Customer(
            id=None,
            name="Transaction Customer",
            phone="9876543210",
            email="transaction@example.com",
            address="Delhi",
            created_at="2026-09-21T20:00:00",
        )

        with pytest.raises(ValueError, match="transaction failed"):
            with transaction(connection):
                repository.add(customer)
                raise ValueError("transaction failed")

        stored_customer = repository.get_by_id(customer.id)

        assert stored_customer is None
    finally:
        connection.close()
