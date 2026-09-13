from datetime import datetime

from application.services.product_service import ProductService
from domain.entities.product import Product
from infrastructure.database.connection import get_connection
from infrastructure.repositories.product_repository import ProductRepository


def create_product_service() -> tuple[ProductService, object]:
    connection = get_connection()
    repository = ProductRepository(connection)
    service = ProductService(repository)
    return service, connection


def add_product(service: ProductService) -> None:
    print()
    print("Add Product")

    name = input("Name: ")
    description = input("Description: ") or None
    sku = input("SKU: ")
    price = float(input("Price: "))
    quantity = int(input("Quantity: "))

    product = Product(
        id=None,
        name=name,
        description=description,
        sku=sku,
        price=price,
        quantity=quantity,
        created_at=datetime.now().isoformat(timespec="seconds"),
    )

    service.add_product(product)

    print(f"Product added successfully with ID: {product.id}")


def list_products(service: ProductService) -> None:
    print()
    print("Product List")

    products = service.get_products()

    if not products:
        print("No products found.")
        return

    for product in products:
        print(
            f"ID: {product.id} | "
            f"Name: {product.name} | "
            f"SKU: {product.sku} | "
            f"Price: {product.price:.2f} | "
            f"Quantity: {product.quantity}"
        )


def get_product(service: ProductService) -> None:
    print()
    print("Get Product")

    product_id = int(input("Product ID: "))
    product = service.get_product(product_id)

    if product is None:
        print("Product not found.")
        return

    print(f"ID: {product.id}")
    print(f"Name: {product.name}")
    print(f"SKU: {product.sku}")
    print(f"Price: {product.price:.2f}")
    print(f"Quantity: {product.quantity}")


def handle_products(service: ProductService | None = None) -> None:
    owns_connection = service is None

    if service is None:
        service, connection = create_product_service()

    try:
        while True:
            print()
            print("Products")
            print("1. Add product")
            print("2. List products")
            print("3. Get product")
            print("4. Delete product")
            print("0. Back")
            print()

            choice = input("Enter your choice: ")

            if choice == "0":
                break

            if choice == "1":
                add_product(service)
            elif choice == "2":
                list_products(service)
            elif choice == "3":
                get_product(service)
            elif choice == "4":
                delete_product(service)
            else:
                print("Invalid choice. Please select a valid option.")
    finally:
        if owns_connection:
            connection.close()


def delete_product(service: ProductService) -> None:
    print()
    print("Delete Product")

    product_id = int(input("Product ID: "))
    service.delete_product(product_id)

    print(f"Product deleted successfully with ID: {product_id}")
