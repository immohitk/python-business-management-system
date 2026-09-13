from datetime import datetime

from application.services.supplier_service import SupplierService
from domain.entities.supplier import Supplier
from infrastructure.database.connection import get_connection
from infrastructure.repositories.supplier_repository import SupplierRepository


def create_supplier_service() -> tuple[SupplierService, object]:
    connection = get_connection()
    repository = SupplierRepository(connection)
    service = SupplierService(repository)
    return service, connection


def add_supplier(service: SupplierService) -> None:
    print()
    print("Add Supplier")

    name = input("Name: ")
    phone = input("Phone: ")
    email = input("Email: ") or None
    address = input("Address: ") or None

    supplier = Supplier(
        id=None,
        name=name,
        phone=phone,
        email=email,
        address=address,
        created_at=datetime.now().isoformat(timespec="seconds"),
    )

    service.add_supplier(supplier)

    print(f"Supplier added successfully with ID: {supplier.id}")


def list_suppliers(service: SupplierService) -> None:
    print()
    print("Supplier List")

    suppliers = service.get_suppliers()

    if not suppliers:
        print("No suppliers found.")
        return

    for supplier in suppliers:
        print(
            f"ID: {supplier.id} | "
            f"Name: {supplier.name} | "
            f"Phone: {supplier.phone or '-'} | "
            f"Email: {supplier.email or '-'}"
        )


def get_supplier(service: SupplierService) -> None:
    print()
    print("Get Supplier")

    supplier_id = int(input("Supplier ID: "))
    supplier = service.get_supplier(supplier_id)

    if supplier is None:
        print("Supplier not found.")
        return

    print(f"ID: {supplier.id}")
    print(f"Name: {supplier.name}")
    print(f"Phone: {supplier.phone or '-'}")
    print(f"Email: {supplier.email or '-'}")
    print(f"Address: {supplier.address or '-'}")


def delete_supplier(service: SupplierService) -> None:
    print()
    print("Delete Supplier")

    supplier_id = int(input("Supplier ID: "))
    service.delete_supplier(supplier_id)

    print(f"Supplier deleted successfully with ID: {supplier_id}")


def handle_suppliers(service: SupplierService | None = None) -> None:
    owns_connection = service is None

    if service is None:
        service, connection = create_supplier_service()

    try:
        while True:
            print()
            print("Suppliers")
            print("1. Add supplier")
            print("2. List suppliers")
            print("3. Get supplier")
            print("4. Delete supplier")
            print("0. Back")
            print()

            choice = input("Enter your choice: ")

            if choice == "0":
                break

            if choice == "1":
                add_supplier(service)
            elif choice == "2":
                list_suppliers(service)
            elif choice == "3":
                get_supplier(service)
            elif choice == "4":
                delete_supplier(service)
            else:
                print("Invalid choice. Please select a valid option.")
    finally:
        if owns_connection:
            connection.close()
