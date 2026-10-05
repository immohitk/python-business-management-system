from application.services.tax_charge_calculator import TaxChargeCalculator
from domain.entities.tax_charge import TaxCharge
from infrastructure.database.connection import get_connection
from infrastructure.database.initialization import initialize_database
from infrastructure.repositories.tax_charge_repository import TaxChargeRepository


def test_calculator_uses_persisted_active_tax_and_charge(tmp_path):
    database_path = tmp_path / "integration.db"
    initialize_database(database_path)

    connection = get_connection(database_path)

    try:
        repository = TaxChargeRepository(connection)

        gst = TaxCharge(
            id=None,
            name="GST",
            type="Tax",
            calculation="Percentage",
            value=18.0,
            scope="Overall",
            product_id=None,
            is_active=True,
            created_at="2026-09-17T22:00:00",
        )

        delivery_charge = TaxCharge(
            id=None,
            name="Delivery Charge",
            type="Charge",
            calculation="Fixed Amount",
            value=100.0,
            scope="Overall",
            product_id=None,
            is_active=True,
            created_at="2026-09-17T22:01:00",
        )

        inactive_charge = TaxCharge(
            id=None,
            name="Inactive Charge",
            type="Charge",
            calculation="Fixed Amount",
            value=50.0,
            scope="Overall",
            product_id=None,
            is_active=False,
            created_at="2026-09-17T22:02:00",
        )

        repository.add(gst)
        repository.add(delivery_charge)
        repository.add(inactive_charge)

        persisted_tax_charges = repository.get_all()
        calculator = TaxChargeCalculator()

        calculated_amounts = [
            calculator.calculate(
                tax_charge,
                base_amount=1000.0,
            )
            for tax_charge in persisted_tax_charges
        ]

        assert calculated_amounts == [180.0, 100.0, 0.0]
        assert sum(calculated_amounts) == 280.0
    finally:
        connection.close()


def test_tax_charge_defaults_are_persisted_and_retrievable(tmp_path):
    database_path = tmp_path / "defaults.db"
    initialize_database(database_path)
    connection = get_connection(database_path)
    try:
        repository = TaxChargeRepository(connection)
        default_gst = TaxCharge(
            id=None, name="GST", type="Tax", calculation="Percentage",
            value=18.0, scope="Overall", product_id=None, is_active=True,
            created_at="2026-10-05T09:00:00", tax_code="GST", is_default=True,
        )
        repository.add(default_gst)
        defaults = repository.get_defaults()
        assert len(defaults) == 1
        assert defaults[0].tax_code == "GST"
        assert defaults[0].is_default is True
    finally:
        connection.close()


def test_sale_tax_charge_snapshot_keeps_historical_value(tmp_path):
    database_path = tmp_path / "snapshot.db"
    initialize_database(database_path)
    connection = get_connection(database_path)
    try:
        repository = TaxChargeRepository(connection)
        gst = TaxCharge(
            id=None, name="GST", type="Tax", calculation="Percentage",
            value=18.0, scope="Overall", product_id=None, is_active=True,
            created_at="2026-10-05T09:00:00", tax_code="GST", is_default=True,
        )
        repository.add(gst)
        repository.snapshot_for_sale(1, gst, 180.0, "2026-10-05T09:01:00")
        gst.value = 5.0
        snapshots = repository.get_sale_snapshots(1)
        assert snapshots[0]["value"] == 18.0
        assert snapshots[0]["amount"] == 180.0
    finally:
        connection.close()
