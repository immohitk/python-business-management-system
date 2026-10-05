from dataclasses import dataclass

from domain.rules.customer_rules import (
    validate_customer_created_at,
    validate_customer_name,
    validate_customer_status,
)


@dataclass
class Customer:
    id: int | None
    name: str
    phone: str | None
    email: str | None
    address: str | None
    created_at: str
    city: str | None = None
    state: str | None = None
    pincode: str | None = None
    status: str = "ACTIVE"

    def __post_init__(self) -> None:
        validate_customer_name(self.name)
        validate_customer_status(self.status)
        validate_customer_created_at(self.created_at)
