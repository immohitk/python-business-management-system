from domain.entities.tax_charge import TaxCharge
from application.services.tax_charge_service import TaxChargeService


class FakeTaxChargeRepository:
    def __init__(self):
        self.added_tax_charge = None
        self.tax_charges = []
        self.updated_tax_charge = None
        self.deleted_tax_charge_id = None

    def add(self, tax_charge):
        self.added_tax_charge = tax_charge

    def get_by_id(self, tax_charge_id):
        for tax_charge in self.tax_charges:
            if tax_charge.id == tax_charge_id:
                return tax_charge
        return None

    def get_all(self):
        return self.tax_charges

    def update(self, tax_charge):
        self.updated_tax_charge = tax_charge

    def delete(self, tax_charge_id):
        self.deleted_tax_charge_id = tax_charge_id


def create_tax_charge() -> TaxCharge:
    return TaxCharge(
        id=1,
        name="GST",
        type="Tax",
        calculation="Percentage",
        value=18.0,
        scope="Overall",
        product_id=None,
        is_active=True,
        created_at="2026-09-16T20:00:00",
    )


def test_add_tax_charge_delegates_to_repository():
    repository = FakeTaxChargeRepository()
    service = TaxChargeService(repository)
    tax_charge = create_tax_charge()

    service.add_tax_charge(tax_charge)

    assert repository.added_tax_charge == tax_charge


def test_get_tax_charge_delegates_to_repository():
    repository = FakeTaxChargeRepository()
    tax_charge = create_tax_charge()
    repository.tax_charges = [tax_charge]
    service = TaxChargeService(repository)

    result = service.get_tax_charge(tax_charge.id)

    assert result == tax_charge


def test_get_tax_charges_delegates_to_repository():
    repository = FakeTaxChargeRepository()
    tax_charges = [create_tax_charge()]
    repository.tax_charges = tax_charges
    service = TaxChargeService(repository)

    result = service.get_tax_charges()

    assert result == tax_charges


def test_update_tax_charge_delegates_to_repository():
    repository = FakeTaxChargeRepository()
    service = TaxChargeService(repository)
    tax_charge = create_tax_charge()

    service.update_tax_charge(tax_charge)

    assert repository.updated_tax_charge == tax_charge


def test_delete_tax_charge_delegates_to_repository():
    repository = FakeTaxChargeRepository()
    service = TaxChargeService(repository)

    service.delete_tax_charge(1)

    assert repository.deleted_tax_charge_id == 1