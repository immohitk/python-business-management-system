from application.services.reporting_service import ReportingService
from infrastructure.database.connection import get_connection
from infrastructure.repositories.reporting_repository import ReportingRepository


def create_reporting_service() -> tuple[ReportingService, object]:
    connection = get_connection()
    repository = ReportingRepository(connection)
    service = ReportingService(repository)

    return service, connection


def handle_reports(service: ReportingService | None = None) -> None:
    owns_connection = service is None

    if service is None:
        service, connection = create_reporting_service()

    try:
        while True:
            print()
            print("Reports")
            print("1. Business summary")
            print("2. Sales reports")
            print("3. Inventory reports")
            print("4. Customer reports")
            print("5. Supplier reports")
            print("0. Back")
            print()

            choice = input("Enter your choice: ")

            if choice == "0":
                break
            if choice == "1":
                show_business_summary(service)
            elif choice == "2":
                show_sales_reports(service)
            elif choice == "3":
                show_inventory_reports(service)
            elif choice == "4":
                show_customer_reports(service)
            elif choice == "5":
                show_supplier_reports(service)
            else:
                print("Invalid choice. Please select a valid option.")
    finally:
        if owns_connection:
            connection.close()


def show_business_summary(service: ReportingService) -> None:
    print()
    print("Business Summary")

    summary = service.get_business_summary()

    for key, value in summary.items():
        print(f"{key}: {value}")


def show_sales_reports(service: ReportingService) -> None:
    print()
    print("Sales Reports")

    print(f"Total sales: {service.get_sales_total():.2f}")

    print()
    print("Sales by Date")
    rows = service.get_sales_by_date()

    if not rows:
        print("No sales found.")
    else:
        for row in rows:
            print(
                f"Date: {row['sale_date']} | "
                f"Sales: {row['sale_count']} | "
                f"Total: {row['total_amount']:.2f}"
            )

    print()
    print("Sales by Product")
    rows = service.get_sales_by_product()

    if not rows:
        print("No product sales found.")
    else:
        for row in rows:
            print(
                f"ID: {row['product_id']} | "
                f"Name: {row['product_name']} | "
                f"Quantity: {row['quantity_sold']} | "
                f"Amount: {row['sales_amount']:.2f}"
            )


def show_inventory_reports(service: ReportingService) -> None:
    print()
    print("Inventory Reports")

    print()
    print("Stock Status")
    rows = service.get_stock_status()

    if not rows:
        print("No products found.")
    else:
        for row in rows:
            print(
                f"ID: {row['product_id']} | "
                f"Name: {row['product_name']} | "
                f"SKU: {row['sku']} | "
                f"Quantity: {row['quantity']}"
            )

    print()
    print("Stock Movement Summary")
    rows = service.get_stock_movements_summary()

    if not rows:
        print("No stock movements found.")
    else:
        for row in rows:
            print(
                f"Type: {row['movement_type']} | "
                f"Movements: {row['movement_count']} | "
                f"Quantity: {row['total_quantity']}"
            )

    print()
    print("Low Stock Products")
    threshold = _read_non_negative_integer("Low stock threshold: ")

    if threshold is None:
        return

    rows = service.get_low_stock_products(threshold)

    if not rows:
        print("No low-stock products found.")
    else:
        for row in rows:
            print(
                f"ID: {row['product_id']} | "
                f"Name: {row['product_name']} | "
                f"SKU: {row['sku']} | "
                f"Quantity: {row['quantity']}"
            )


def show_customer_reports(service: ReportingService) -> None:
    print()
    print("Customer Reports")

    rows = service.get_customers_summary()

    if not rows:
        print("No customers found.")
        return

    for row in rows:
        print(
            f"ID: {row['customer_id']} | "
            f"Name: {row['customer_name']} | "
            f"Phone: {row['phone']} | "
            f"Email: {row['email']}"
        )


def show_supplier_reports(service: ReportingService) -> None:
    print()
    print("Supplier Reports")

    rows = service.get_suppliers_summary()

    if not rows:
        print("No suppliers found.")
        return

    for row in rows:
        print(
            f"ID: {row['supplier_id']} | "
            f"Name: {row['supplier_name']} | "
            f"Phone: {row['phone']} | "
            f"Email: {row['email']}"
        )


def _read_non_negative_integer(prompt: str) -> int | None:
    try:
        value = int(input(prompt))
    except ValueError:
        print("Please enter a valid integer.")
        return None

    if value < 0:
        print("Please enter a non-negative integer.")
        return None

    return value
