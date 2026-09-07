from dataclasses import dataclass


@dataclass
class Product:
    id: int | None
    name: str
    description: str | None
    sku: str
    price: float
    quantity: int
    created_at: str