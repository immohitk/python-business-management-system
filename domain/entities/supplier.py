from dataclasses import dataclass

from domain.rules.supplier_rules import (
    validate_supplier_created_at,
    validate_supplier_name,
)


@dataclass
class Supplier:
    id: int | None
    name: str
    phone: str | None
    email: str | None
    address: str | None
    created_at: str

    def __post_init__(self) -> None:
        validate_supplier_name(self.name)
        validate_supplier_created_at(self.created_at)
