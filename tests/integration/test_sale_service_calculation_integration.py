from application.services.sale_calculation_service import SaleCalculationService
from application.services.tax_charge_calculator import TaxChargeCalculator
from domain.entities.sale import Sale
from domain.entities.sale_line import SaleLine
from domain.entities.tax_charge import TaxCharge


def test_sale_calculation_with_tax_and_charge() -> None:
    sale = Sale(
        id=None,
        customer_id=1,
        sale_date="2026-10-04",
        total_amount=0.0,
        created_at="2026-10-04T21:00:00",
        lines=[
            SaleLine(
                product_id=1,
                quantity=2,
                unit_price=500.0,
            ),
        ],
    )

    tax = TaxCharge(
        id=1,
        name="GST",
        type="Tax",
        calculation="Percentage",
        value=18.0,
        scope="Overall",
        product_id=None,
        is_active=True,
        created_at="2026-10-04T21:00:00",
    )

    charge = TaxCharge(
        id=2,
        name="Delivery Charge",
        type="Charge",
        calculation="Fixed Amount",
        value=50.0,
        scope="Overall",
        product_id=None,
        is_active=True,
        created_at="2026-10-04T21:00:00",
    )

    service = SaleCalculationService(TaxChargeCalculator())

    result = service.calculate(
        sale=sale,
        tax_charges=[tax, charge],
    )

    assert result.subtotal == 1000.0
    assert result.tax_total == 180.0
    assert result.charge_total == 50.0
    assert result.final_total == 1230.0