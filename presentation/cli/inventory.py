from application.services.inventory_service import InventoryService
from infrastructure.database.connection import get_connection
from infrastructure.repositories.product_repository import ProductRepository
from infrastructure.repositories.stock_movement_repository import (
    StockMovementRepository,
)


def create_inventory_service() -> tuple[InventoryService, object]:
    connection = get_connection()

    product_repository = ProductRepository(connection)
    stock_movement_repository = StockMovementRepository(connection)

    service = InventoryService(
        product_repository,
        stock_movement_repository,
    )

    return service, connection


def handle_inventory(service: InventoryService | None = None) -> None:
    owns_connection = service is None

    if service is None:
        service, connection = create_inventory_service()

    try:
        while True:
            print()
            print("Inventory")
            print("1. View stock")
            print("2. Stock in")
            print("3. Adjust stock")
            print("4. Stock out")
            print("5. View movement history")
            print("0. Back")
            print()

            choice = input("Enter your choice: ")

            if choice == "0":
                break

            if choice == "1":
                print("View stock")
            elif choice == "2":
                print("Stock in")
            elif choice == "3":
                print("Adjust stock")
            elif choice == "4":
                print("Stock out")
            elif choice == "5":
                print("View movement history")
            else:
                print("Invalid choice. Please select a valid option.")
    finally:
        if owns_connection:
            connection.close()
