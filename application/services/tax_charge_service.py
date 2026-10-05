from domain.entities.tax_charge import TaxCharge
from infrastructure.repositories.tax_charge_repository import TaxChargeRepository


class TaxChargeService:
    """Application service for TaxCharge operations."""

    def __init__(self, repository: TaxChargeRepository) -> None:
        self.repository = repository

    def add_tax_charge(self, tax_charge: TaxCharge) -> None:
        self.repository.add(tax_charge)

    def get_tax_charge(self, tax_charge_id: int) -> TaxCharge | None:
        return self.repository.get_by_id(tax_charge_id)

    def get_tax_charges(self) -> list[TaxCharge]:
        return self.repository.get_all()

    def get_default_tax_charges(self) -> list[TaxCharge]:
        return self.repository.get_defaults()

    def update_tax_charge(self, tax_charge: TaxCharge) -> None:
        self.repository.update(tax_charge)

    def delete_tax_charge(self, tax_charge_id: int) -> None:
        self.repository.delete(tax_charge_id)