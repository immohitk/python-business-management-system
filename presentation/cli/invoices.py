from application.invoice.formatter import InvoiceFormatter
from application.services.invoice_presentation_service import (
    InvoicePresentationService,
)
from infrastructure.database.connection import get_connection
from infrastructure.repositories.customer_repository import CustomerRepository
from infrastructure.repositories.invoice_repository import InvoiceRepository
from infrastructure.repositories.product_repository import ProductRepository
from infrastructure.repositories.sale_repository import SaleRepository


def create_invoice_presentation_service() -> tuple[
    InvoicePresentationService,
    object,
]:
    connection = get_connection()

    invoice_repository = InvoiceRepository(connection)
    sale_repository = SaleRepository(connection)
    customer_repository = CustomerRepository(connection)
    product_repository = ProductRepository(connection)

    service = InvoicePresentationService(
        invoice_repository=invoice_repository,
        sale_repository=sale_repository,
        customer_repository=customer_repository,
        product_repository=product_repository,
    )

    return service, connection


def show_invoice(
    service: InvoicePresentationService,
    formatter: InvoiceFormatter | None = None,
) -> None:
    print()
    print("Show Invoice")

    if formatter is None:
        formatter = InvoiceFormatter()

    try:
        invoice_id = int(input("Invoice ID: "))

        invoice = service.get_invoice_presentation(invoice_id)

        print()
        print(formatter.format(invoice))

    except ValueError as exc:
        print(str(exc))


def handle_invoices(
    service: InvoicePresentationService | None = None,
) -> None:
    owns_connection = service is None

    if service is None:
        service, connection = create_invoice_presentation_service()

    try:
        while True:
            print()
            print("Invoices")
            print("1. Show invoice")
            print("0. Back")
            print()

            choice = input("Enter your choice: ")

            if choice == "0":
                break

            if choice == "1":
                show_invoice(service)
            else:
                print("Invalid choice. Please select a valid option.")
    finally:
        if owns_connection:
            connection.close()
