from pathlib import Path

from application.services.reporting_service import ReportingService
from application.services.customer_service import CustomerService
from application.services.supplier_service import SupplierService
from domain.entities.customer import Customer
from domain.entities.supplier import Supplier
from infrastructure.database.connection import get_connection
from infrastructure.database.initialization import initialize_database
from infrastructure.repositories.reporting_repository import ReportingRepository
from infrastructure.repositories.customer_repository import CustomerRepository
from infrastructure.repositories.supplier_repository import SupplierRepository


def create_service(tmp_path: Path) -> tuple[ReportingService, object]:
    database_path = tmp_path / "test.db"
    initialize_database(database_path)
    connection = get_connection(database_path)
    repository = ReportingRepository(connection)

    return ReportingService(repository), connection


def seed_customer_supplier_data(connection) -> None:
    connection.executemany(
        """
        INSERT INTO customers (
            name,
            phone,
            email,
            address,
            created_at
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        [
            (
                "Customer A",
                "1111111111",
                "a@example.com",
                "Address A",
                "2026-09-28T10:00:00",
            ),
            (
                "Customer B",
                "2222222222",
                "b@example.com",
                "Address B",
                "2026-09-28T10:05:00",
            ),
        ],
    )

    connection.executemany(
        """
        INSERT INTO suppliers (
            name,
            phone,
            email,
            address,
            created_at
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        [
            (
                "Supplier A",
                "3333333333",
                "supplier-a@example.com",
                "Supplier Address A",
                "2026-09-28T10:10:00",
            ),
            (
                "Supplier B",
                "4444444444",
                "supplier-b@example.com",
                "Supplier Address B",
                "2026-09-28T10:15:00",
            ),
        ],
    )

    connection.commit()


def test_customer_and_supplier_reporting_works_through_real_database(
    tmp_path,
):
    service, connection = create_service(tmp_path)

    try:
        seed_customer_supplier_data(connection)

        assert service.get_customers_summary() == [
            {
                "customer_id": 1,
                "customer_name": "Customer A",
                "phone": "1111111111",
                "email": "a@example.com",
            },
            {
                "customer_id": 2,
                "customer_name": "Customer B",
                "phone": "2222222222",
                "email": "b@example.com",
            },
        ]

        assert service.get_suppliers_summary() == [
            {
                "supplier_id": 1,
                "supplier_name": "Supplier A",
                "phone": "3333333333",
                "email": "supplier-a@example.com",
            },
            {
                "supplier_id": 2,
                "supplier_name": "Supplier B",
                "phone": "4444444444",
                "email": "supplier-b@example.com",
            },
        ]
    finally:
        connection.close()


def test_customer_and_supplier_services_integrate_with_reporting(
    tmp_path,
):
    database_path = tmp_path / "test.db"
    initialize_database(database_path)
    connection = get_connection(database_path)

    try:
        customer_repository = CustomerRepository(connection)
        supplier_repository = SupplierRepository(connection)
        reporting_repository = ReportingRepository(connection)

        customer_service = CustomerService(customer_repository)
        supplier_service = SupplierService(supplier_repository)
        reporting_service = ReportingService(reporting_repository)

        customer = Customer(
            id=None,
            name="Application Customer",
            phone="9999999999",
            email="application.customer@example.com",
            address="Bengaluru",
            created_at="2026-09-30T10:00:00",
        )

        supplier = Supplier(
            id=None,
            name="Application Supplier",
            phone="8888888888",
            email="application.supplier@example.com",
            address="Bengaluru",
            created_at="2026-09-30T10:05:00",
        )

        customer_service.add_customer(customer)
        supplier_service.add_supplier(supplier)

        assert reporting_service.get_customers_summary() == [
            {
                "customer_id": customer.id,
                "customer_name": "Application Customer",
                "phone": "9999999999",
                "email": "application.customer@example.com",
            }
        ]

        assert reporting_service.get_suppliers_summary() == [
            {
                "supplier_id": supplier.id,
                "supplier_name": "Application Supplier",
                "phone": "8888888888",
                "email": "application.supplier@example.com",
            }
        ]

    finally:
        connection.close()
