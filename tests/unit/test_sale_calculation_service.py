from domain.entities.sale import Sale
from domain.entities.sale_line import SaleLine
from domain.entities.tax_charge import TaxCharge
from application.services.sale_calculation_service import SaleCalculationService
from application.services.tax_charge_calculator import TaxChargeCalculator


def make_sale(lines: list[SaleLine]) -> Sale:
    return Sale(
        id=None,
        customer_id=1,
        sale_date="2026-10-04",
        total_amount=0.0,
        created_at="2026-10-04T01:00:00",
        lines=lines,
    )


def make_tax_charge(
    name: str,
    tax_charge_type: str,
    calculation: str,
    value: float,
    scope: str,
    product_id: int | None = None,
    is_active: bool = True,
) -> TaxCharge:
    return TaxCharge(
        id=None,
        name=name,
        type=tax_charge_type,
        calculation=calculation,
        value=value,
        scope=scope,
        product_id=product_id,
        is_active=is_active,
        created_at="2026-10-04T01:00:00",
    )


def test_calculates_subtotal_without_taxes_or_charges() -> None:
    sale = make_sale(
        [
            SaleLine(product_id=1, quantity=2, unit_price=100.0),
            SaleLine(product_id=2, quantity=3, unit_price=50.0),
        ]
    )

    service = SaleCalculationService(TaxChargeCalculator())

    result = service.calculate(sale, [])

    assert result.subtotal == 350.0
    assert result.tax_total == 0.0
    assert result.charge_total == 0.0
    assert result.final_total == 350.0


def test_calculates_overall_percentage_tax() -> None:
    sale = make_sale(
        [SaleLine(product_id=1, quantity=2, unit_price=100.0)]
    )

    gst = make_tax_charge(
        "GST",
        "Tax",
        "Percentage",
        18.0,
        "Overall",
    )

    service = SaleCalculationService(TaxChargeCalculator())

    result = service.calculate(sale, [gst])

    assert result.subtotal == 200.0
    assert result.tax_total == 36.0
    assert result.charge_total == 0.0
    assert result.final_total == 236.0


def test_calculates_overall_fixed_charge() -> None:
    sale = make_sale(
        [SaleLine(product_id=1, quantity=2, unit_price=100.0)]
    )

    delivery = make_tax_charge(
        "Delivery Charge",
        "Charge",
        "Fixed Amount",
        50.0,
        "Overall",
    )

    service = SaleCalculationService(TaxChargeCalculator())

    result = service.calculate(sale, [delivery])

    assert result.subtotal == 200.0
    assert result.tax_total == 0.0
    assert result.charge_total == 50.0
    assert result.final_total == 250.0


def test_calculates_product_percentage_tax() -> None:
    sale = make_sale(
        [
            SaleLine(product_id=1, quantity=2, unit_price=100.0),
            SaleLine(product_id=2, quantity=1, unit_price=200.0),
        ]
    )

    product_tax = make_tax_charge(
        "Product GST",
        "Tax",
        "Percentage",
        12.0,
        "Product",
        product_id=1,
    )

    service = SaleCalculationService(TaxChargeCalculator())

    result = service.calculate(sale, [product_tax])

    assert result.subtotal == 400.0
    assert result.tax_total == 24.0
    assert result.charge_total == 0.0
    assert result.final_total == 424.0


def test_calculates_product_fixed_charge() -> None:
    sale = make_sale(
        [
            SaleLine(product_id=1, quantity=2, unit_price=100.0),
            SaleLine(product_id=2, quantity=1, unit_price=200.0),
        ]
    )

    packaging = make_tax_charge(
        "Packaging Fee",
        "Charge",
        "Fixed Amount",
        25.0,
        "Product",
        product_id=1,
    )

    service = SaleCalculationService(TaxChargeCalculator())

    result = service.calculate(sale, [packaging])

    assert result.subtotal == 400.0
    assert result.tax_total == 0.0
    assert result.charge_total == 25.0
    assert result.final_total == 425.0


def test_ignores_inactive_tax_or_charge() -> None:
    sale = make_sale(
        [SaleLine(product_id=1, quantity=2, unit_price=100.0)]
    )

    inactive_tax = make_tax_charge(
        "GST",
        "Tax",
        "Percentage",
        18.0,
        "Overall",
        is_active=False,
    )

    service = SaleCalculationService(TaxChargeCalculator())

    result = service.calculate(sale, [inactive_tax])

    assert result.subtotal == 200.0
    assert result.tax_total == 0.0
    assert result.charge_total == 0.0
    assert result.final_total == 200.0


def test_calculates_multiple_taxes_and_charges() -> None:
    sale = make_sale(
        [SaleLine(product_id=1, quantity=2, unit_price=100.0)]
    )

    gst = make_tax_charge(
        "GST",
        "Tax",
        "Percentage",
        18.0,
        "Overall",
    )

    service_charge = make_tax_charge(
        "Service Charge",
        "Charge",
        "Percentage",
        5.0,
        "Overall",
    )

    packaging = make_tax_charge(
        "Packaging Fee",
        "Charge",
        "Fixed Amount",
        20.0,
        "Overall",
    )

    service = SaleCalculationService(TaxChargeCalculator())

    result = service.calculate(
        sale,
        [gst, service_charge, packaging],
    )

    assert result.subtotal == 200.0
    assert result.tax_total == 36.0
    assert result.charge_total == 30.0
    assert result.final_total == 266.0
