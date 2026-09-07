from dataclasses import dataclass


@dataclass
class Sale:
    id: int | None
    customer_id: int
    sale_date: str
    total_amount: float
    created_at: str