from domain.entities.tax_charge import TaxCharge
from application.services.tax_charge_calculator import TaxChargeCalculator


def create_tax_charge(
    *,
    name="GST",
    tax_charge_type="Tax",
    calculation="Percentage",
    value=18.0,
    scope="Overall",
    product_id=None,
    is_active=True,
):
    return TaxCharge(
        id=1,
        name=name,
        type=tax_charge_type,
        calculation=calculation,
        value=value,
        scope=scope,
        product_id=product_id,
        is_active=is_active,
        created_at="2026-09-17T20:00:00",
    )


def test_percentage_overall_calculation():
    calculator = TaxChargeCalculator()
    tax_charge = create_tax_charge()

    result = calculator.calculate(
        tax_charge,
        base_amount=1000.0,
    )

    assert result == 180.0


def test_fixed_amount_overall_calculation():
    calculator = TaxChargeCalculator()
    charge = create_tax_charge(
        name="Delivery Charge",
        tax_charge_type="Charge",
        calculation="Fixed Amount",
        value=100.0,
    )

    result = calculator.calculate(
        charge,
        base_amount=1000.0,
    )

    assert result == 100.0


def test_percentage_product_calculation_for_matching_product():
    calculator = TaxChargeCalculator()
    tax_charge = create_tax_charge(
        scope="Product",
        product_id=5,
    )

    result = calculator.calculate(
        tax_charge,
        base_amount=500.0,
        product_id=5,
    )

    assert result == 90.0


def test_product_calculation_returns_zero_for_non_matching_product():
    calculator = TaxChargeCalculator()
    tax_charge = create_tax_charge(
        scope="Product",
        product_id=5,
    )

    result = calculator.calculate(
        tax_charge,
        base_amount=500.0,
        product_id=10,
    )

    assert result == 0.0


def test_inactive_tax_charge_returns_zero():
    calculator = TaxChargeCalculator()
    tax_charge = create_tax_charge(
        is_active=False,
    )

    result = calculator.calculate(
        tax_charge,
        base_amount=1000.0,
    )

    assert result == 0.0


def test_zero_percentage_returns_zero():
    calculator = TaxChargeCalculator()
    tax_charge = create_tax_charge(value=0.0)

    result = calculator.calculate(
        tax_charge,
        base_amount=1000.0,
    )

    assert result == 0.0


def test_zero_fixed_amount_returns_zero():
    calculator = TaxChargeCalculator()
    charge = create_tax_charge(
        name="Free Delivery",
        tax_charge_type="Charge",
        calculation="Fixed Amount",
        value=0.0,
    )

    result = calculator.calculate(
        charge,
        base_amount=1000.0,
    )

    assert result == 0.0


def test_decimal_percentage_calculation():
    calculator = TaxChargeCalculator()
    tax_charge = create_tax_charge(value=2.5)

    result = calculator.calculate(
        tax_charge,
        base_amount=1000.0,
    )

    assert result == 25.0


def test_decimal_fixed_amount_calculation():
    calculator = TaxChargeCalculator()
    charge = create_tax_charge(
        name="Handling Charge",
        tax_charge_type="Charge",
        calculation="Fixed Amount",
        value=49.50,
    )

    result = calculator.calculate(
        charge,
        base_amount=1000.0,
    )

    assert result == 49.50


def test_zero_base_amount_returns_zero_for_percentage():
    calculator = TaxChargeCalculator()
    tax_charge = create_tax_charge(value=18.0)

    result = calculator.calculate(
        tax_charge,
        base_amount=0.0,
    )

    assert result == 0.0
