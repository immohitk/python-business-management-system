from datetime import datetime

from application.services.customer_service import CustomerService
from domain.entities.customer import Customer
from infrastructure.database.connection import get_connection
from infrastructure.repositories.customer_repository import CustomerRepository


def create_customer_service() -> tuple[CustomerService, object]:
    connection = get_connection()
    repository = CustomerRepository(connection)
    service = CustomerService(repository)
    return service, connection


def add_customer(service: CustomerService) -> None:
    print()
    print("Add Customer")

    name = input("Name: ")
    phone = input("Phone: ")
    email = input("Email: ") or None
    address = input("Address: ") or None

    customer = Customer(
        id=None,
        name=name,
        phone=phone,
        email=email,
        address=address,
        created_at=datetime.now().isoformat(timespec="seconds"),
    )

    service.add_customer(customer)

    print(f"Customer added successfully with ID: {customer.id}")


def list_customers(service: CustomerService) -> None:
    print()
    print("Customer List")

    customers = service.get_customers()

    if not customers:
        print("No customers found.")
        return

    for customer in customers:
        print(
            f"ID: {customer.id} | "
            f"Name: {customer.name} | "
            f"Phone: {customer.phone or '-'} | "
            f"Email: {customer.email or '-'}"
        )


def get_customer(service: CustomerService) -> None:
    print()
    print("Get Customer")

    customer_id = int(input("Customer ID: "))
    customer = service.get_customer(customer_id)

    if customer is None:
        print("Customer not found.")
        return

    print(f"ID: {customer.id}")
    print(f"Name: {customer.name}")
    print(f"Phone: {customer.phone or '-'}")
    print(f"Email: {customer.email or '-'}")
    print(f"Address: {customer.address or '-'}")


def delete_customer(service: CustomerService) -> None:
    print()
    print("Delete Customer")

    customer_id = int(input("Customer ID: "))
    service.delete_customer(customer_id)

    print(f"Customer deleted successfully with ID: {customer_id}")


def handle_customers(service: CustomerService | None = None) -> None:
    owns_connection = service is None

    if service is None:
        service, connection = create_customer_service()

    try:
        while True:
            print()
            print("Customers")
            print("1. Add customer")
            print("2. List customers")
            print("3. Get customer")
            print("4. Delete customer")
            print("0. Back")
            print()

            choice = input("Enter your choice: ")

            if choice == "0":
                break

            if choice == "1":
                add_customer(service)
            elif choice == "2":
                list_customers(service)
            elif choice == "3":
                get_customer(service)
            elif choice == "4":
                delete_customer(service)
            else:
                print("Invalid choice. Please select a valid option.")
    finally:
        if owns_connection:
            connection.close()
