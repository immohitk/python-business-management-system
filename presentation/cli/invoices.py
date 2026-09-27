from application.invoice.formatter import InvoiceFormatter
from application.services.invoice_presentation_service import (
    InvoicePresentationService,
)
from application.services.invoice_service import InvoiceService
from application.services.sale_invoice_service import SaleInvoiceService
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


def create_invoice_creation_service() -> tuple[
    SaleInvoiceService,
    object,
]:
    connection = get_connection()

    invoice_repository = InvoiceRepository(connection)
    sale_repository = SaleRepository(connection)

    invoice_service = InvoiceService(invoice_repository)

    service = SaleInvoiceService(
        sale_repository=sale_repository,
        invoice_service=invoice_service,
    )

    return service, connection


def create_invoice_from_sale(
    service: SaleInvoiceService,
) -> None:
    print()
    print("Create Invoice From Sale")

    try:
        sale_id = int(input("Sale ID: "))

        invoice = service.create_invoice_for_sale(sale_id)

        print()
        print(
            f"Invoice created successfully: "
            f"{invoice.invoice_number}"
        )

    except ValueError as exc:
        print(str(exc))


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
    invoice_creation_service: SaleInvoiceService | None = None,
) -> None:
    owns_connection = service is None
    creation_connection = None

    if service is None:
        service, connection = create_invoice_presentation_service()

        if invoice_creation_service is None:
            (
                invoice_creation_service,
                creation_connection,
            ) = create_invoice_creation_service()

    try:
        while True:
            print()
            print("Invoices")
            print("1. Create invoice from sale")
            print("2. Show invoice")
            print("0. Back")
            print()

            choice = input("Enter your choice: ")

            if choice == "0":
                break

            if choice == "1":
                if invoice_creation_service is None:
                    print("Invoice creation service is not available.")
                else:
                    create_invoice_from_sale(invoice_creation_service)

            elif choice == "2":
                show_invoice(service)

            else:
                print("Invalid choice. Please select a valid option.")
    finally:
        if owns_connection:
            connection.close()

        if creation_connection is not None:
            creation_connection.close()
