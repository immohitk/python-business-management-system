from dataclasses import dataclass

from domain.rules.customer_rules import (
    validate_customer_created_at,
    validate_customer_name,
)


@dataclass
class Customer:
    id: int | None
    name: str
    phone: str | None
    email: str | None
    address: str | None
    created_at: str

    def __post_init__(self) -> None:
        validate_customer_name(self.name)
        validate_customer_created_at(self.created_at)
