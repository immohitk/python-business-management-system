from datetime import datetime

from application.services.invoice_service import InvoiceService
from domain.entities.invoice import Invoice
from infrastructure.repositories.sale_repository import SaleRepository


class SaleInvoiceService:
    """Application service for creating invoices from existing sales."""

    def __init__(
        self,
        sale_repository: SaleRepository,
        invoice_service: InvoiceService,
    ) -> None:
        self.sale_repository = sale_repository
        self.invoice_service = invoice_service

    def create_invoice_for_sale(self, sale_id: int) -> Invoice:
        sale = self.sale_repository.get_by_id(sale_id)

        if sale is None:
            raise ValueError("Sale not found")

        invoice = Invoice(
            id=None,
            sale_id=sale.id,
            invoice_number="PENDING",
            invoice_date=sale.sale_date,
            total_amount=sale.total_amount,
            created_at=datetime.now().isoformat(),
        )

        return self.invoice_service.create_invoice(invoice)
