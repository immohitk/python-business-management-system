from datetime import datetime

from application.services.inventory_service import InventoryService
from application.services.sale_service import SaleService
from domain.entities.sale import Sale
from domain.entities.sale_line import SaleLine
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


def create_sale(service: SaleService) -> None:
    print()
    print("Create Sale")

    try:
        customer_id = int(input("Customer ID: "))
        sale_date = input("Sale Date: ")

        lines: list[SaleLine] = []

        while True:
            product_id = int(input("Product ID: "))
            quantity = int(input("Quantity: "))
            unit_price = float(input("Unit Price: "))

            lines.append(
                SaleLine(
                    product_id=product_id,
                    quantity=quantity,
                    unit_price=unit_price,
                )
            )

            add_another = input("Add another line? (y/n): ").strip().lower()

            if add_another != "y":
                break

        created_at = datetime.now().isoformat(timespec="seconds")

        sale = Sale(
            id=None,
            customer_id=customer_id,
            sale_date=sale_date,
            total_amount=0.0,
            created_at=created_at,
            lines=lines,
        )

        service.create_sale(sale)

        print(
            f"Sale created successfully with ID: {sale.id} "
            f"and total: {sale.total_amount:.2f}"
        )

    except ValueError as exc:
        print(str(exc))


def list_sales(service: SaleService) -> None:
    print()
    print("Sales List")
    print()

    sales = service.get_sales()

    if not sales:
        print("No sales found.")
        return

    for sale in sales:
        print(f"ID: {sale.id}")
        print(f"Customer ID: {sale.customer_id}")
        print(f"Sale Date: {sale.sale_date}")
        print(f"Total: {sale.total_amount:.2f}")
        print()


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
                create_sale(service)
            elif choice == "2":
                list_sales(service)
            else:
                print("Invalid choice. Please select a valid option.")
    finally:
        if owns_connection:
            connection.close()
