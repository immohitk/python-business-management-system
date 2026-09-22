from application.services.inventory_service import InventoryService
from application.services.sale_service import SaleService
from infrastructure.database.connection import get_connection
from infrastructure.repositories.product_repository import ProductRepository
from infrastructure.repositories.sale_repository import SaleRepository
from infrastructure.repositories.stock_movement_repository import (
    StockMovementRepository,
)


def create_sale_service() -> tuple[SaleService, object]:
    connection = get_connection()

    sale_repository = SaleRepository(connection)

    product_repository = ProductRepository(connection)
    stock_movement_repository = StockMovementRepository(connection)

    inventory_service = InventoryService(
        product_repository,
        stock_movement_repository,
    )

    service = SaleService(
        sale_repository,
        inventory_service,
    )

    return service, connection


def handle_sales(service: SaleService | None = None) -> None:
    owns_connection = service is None

    if service is None:
        service, connection = create_sale_service()

    try:
        while True:
            print()
            print("Sales")
            print("1. Create sale")
            print("2. List sales")
            print("0. Back")
            print()

            choice = input("Enter your choice: ")

            if choice == "0":
                break

            if choice == "1":
                print("Sale creation will be implemented in the next topic.")
            elif choice == "2":
                print("Sale listing will be implemented in the next topic.")
            else:
                print("Invalid choice. Please select a valid option.")
    finally:
        if owns_connection:
            connection.close()
