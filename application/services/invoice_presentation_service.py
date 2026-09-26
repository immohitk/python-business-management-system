from application.invoice.presentation import (
    CustomerPresentation,
    InvoiceLinePresentation,
    InvoicePresentation,
)
from infrastructure.repositories.customer_repository import CustomerRepository
from infrastructure.repositories.invoice_repository import InvoiceRepository
from infrastructure.repositories.product_repository import ProductRepository
from infrastructure.repositories.sale_repository import SaleRepository


class InvoicePresentationService:
    """Builds presentation data for invoices."""

    def __init__(
        self,
        invoice_repository: InvoiceRepository,
        sale_repository: SaleRepository,
        customer_repository: CustomerRepository,
        product_repository: ProductRepository,
    ) -> None:
        self.invoice_repository = invoice_repository
        self.sale_repository = sale_repository
        self.customer_repository = customer_repository
        self.product_repository = product_repository

    def get_invoice_presentation(
        self,
        invoice_id: int,
    ) -> InvoicePresentation:
        invoice = self.invoice_repository.get_by_id(invoice_id)

        if invoice is None:
            raise ValueError("Invoice not found")

        sale = self.sale_repository.get_by_id(invoice.sale_id)

        if sale is None:
            raise ValueError("Sale not found for invoice")

        customer = self.customer_repository.get_by_id(sale.customer_id)

        if customer is None:
            raise ValueError("Customer not found for sale")

        customer_presentation = CustomerPresentation(
            name=customer.name,
            address=customer.address,
            phone=customer.phone,
            email=customer.email,
        )

        lines = []

        for sale_line in sale.lines:
            product = self.product_repository.get_by_id(sale_line.product_id)

            if product is None:
                raise ValueError(
                    f"Product not found: {sale_line.product_id}"
                )

            lines.append(
                InvoiceLinePresentation(
                    product_name=product.name,
                    sku=product.sku,
                    quantity=sale_line.quantity,
                    unit_price=sale_line.unit_price,
                    amount=sale_line.subtotal,
                )
            )

        return InvoicePresentation(
            invoice_number=invoice.invoice_number,
            invoice_date=invoice.invoice_date,
            sale_id=invoice.sale_id,
            customer=customer_presentation,
            lines=lines,
            total_amount=invoice.total_amount,
        )