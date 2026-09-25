from dataclasses import dataclass


@dataclass
class CustomerPresentation:
    name: str
    address: str | None
    phone: str | None
    email: str | None


@dataclass
class InvoiceLinePresentation:
    product_name: str
    sku: str
    quantity: int
    unit_price: float
    amount: float


@dataclass
class InvoicePresentation:
    invoice_number: str
    invoice_date: str
    sale_id: int
    customer: CustomerPresentation
    lines: list[InvoiceLinePresentation]
    total_amount: float
