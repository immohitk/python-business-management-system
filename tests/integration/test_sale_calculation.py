from application.services.sale_calculation_service import SaleCalculationService
from application.services.tax_charge_calculator import TaxChargeCalculator
from domain.entities.sale import Sale
from domain.entities.sale_line import SaleLine
from domain.entities.tax_charge import TaxCharge


def test_sale_calculation_with_overall_and_product_tax() -> None:
    sale = Sale(
        id=None,
        customer_id=1,
        sale_date="2026-10-04",
        total_amount=0.0,
        created_at="2026-10-04T01:00:00",
        lines=[
            SaleLine(product_id=1, quantity=2, unit_price=100.0),
            SaleLine(product_id=2, quantity=1, unit_price=200.0),
        ],
    )

    overall_gst = TaxCharge(
        id=None,
        name="GST",
        type="Tax",
        calculation="Percentage",
        value=18.0,
        scope="Overall",
        product_id=None,
        is_active=True,
        created_at="2026-10-04T01:00:00",
    )

    product_gst = TaxCharge(
        id=None,
        name="Product GST",
        type="Tax",
        calculation="Percentage",
        value=12.0,
        scope="Product",
        product_id=1,
        is_active=True,
        created_at="2026-10-04T01:00:00",
    )

    service = SaleCalculationService(TaxChargeCalculator())

    result = service.calculate(
        sale,
        [overall_gst, product_gst],
    )

    assert result.subtotal == 400.0
    assert result.tax_total == 96.0
    assert result.charge_total == 0.0
    assert result.final_total == 496.0
