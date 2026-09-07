from dataclasses import dataclass


@dataclass
class Invoice:
    id: int | None
    sale_id: int
    invoice_number: str
    invoice_date: str
    total_amount: float
    created_at: str