from dataclasses import dataclass


@dataclass
class Supplier:
    id: int | None
    name: str
    phone: str | None
    email: str | None
    address: str | None
    created_at: str