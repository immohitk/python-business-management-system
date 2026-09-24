from infrastructure.repositories.invoice_repository import InvoiceRepository


class InvoiceService:
    """Application service for invoice operations."""

    def __init__(self, invoice_repository: InvoiceRepository) -> None:
        self.invoice_repository = invoice_repository

    def generate_invoice_number(self) -> str:
        latest_number = self.invoice_repository.get_latest_invoice_number()

        if latest_number is None:
            return "INV-000001"

        if not latest_number.startswith("INV-"):
            raise ValueError("Invalid invoice number format")

        sequence_text = latest_number.removeprefix("INV-")

        if not sequence_text.isdigit():
            raise ValueError("Invalid invoice number format")

        sequence = int(sequence_text)

        return f"INV-{sequence + 1:06d}"
