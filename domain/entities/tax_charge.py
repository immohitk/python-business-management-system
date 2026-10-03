from dataclasses import dataclass

from domain.rules.tax_charge_rules import (
    validate_tax_charge_calculation,
    validate_tax_charge_created_at,
    validate_tax_charge_name,
    validate_tax_charge_scope,
    validate_tax_charge_type,
    validate_tax_charge_value,
)


@dataclass
class TaxCharge:
    id: int | None
    name: str
    type: str
    calculation: str
    value: float
    scope: str
    product_id: int | None
    is_active: bool
    created_at: str

    def __post_init__(self) -> None:
        validate_tax_charge_name(self.name)
        validate_tax_charge_type(self.type)
        validate_tax_charge_calculation(self.calculation)
        validate_tax_charge_value(self.value)
        validate_tax_charge_scope(self.scope, self.product_id)
        validate_tax_charge_created_at(self.created_at)