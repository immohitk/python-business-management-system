import pytest

from domain.entities.tax_charge import TaxCharge


def make_tax_charge(**overrides) -> TaxCharge:
    data = {
        "id": None,
        "name": "GST",
        "type": "Tax",
        "calculation": "Percentage",
        "value": 18.0,
        "scope": "Overall",
        "product_id": None,
        "is_active": True,
        "created_at": "2026-10-03 10:00:00",
    }
    data.update(overrides)
    return TaxCharge(**data)


def test_valid_overall_tax():
    tax_charge = make_tax_charge()

    assert tax_charge.name == "GST"
    assert tax_charge.type == "Tax"
    assert tax_charge.calculation == "Percentage"
    assert tax_charge.value == 18.0
    assert tax_charge.scope == "Overall"
    assert tax_charge.product_id is None
    assert tax_charge.is_active is True


def test_valid_product_tax():
    tax_charge = make_tax_charge(
        name="Product GST",
        scope="Product",
        product_id=1,
    )

    assert tax_charge.scope == "Product"
    assert tax_charge.product_id == 1


def test_valid_charge():
    tax_charge = make_tax_charge(
        name="Delivery Charge",
        type="Charge",
        calculation="Fixed Amount",
        value=50.0,
    )

    assert tax_charge.type == "Charge"
    assert tax_charge.calculation == "Fixed Amount"
    assert tax_charge.value == 50.0


def test_empty_name_is_rejected():
    with pytest.raises(ValueError, match="name cannot be empty"):
        make_tax_charge(name="   ")


def test_invalid_type_is_rejected():
    with pytest.raises(ValueError, match="type must be Tax or Charge"):
        make_tax_charge(type="Discount")


def test_invalid_calculation_is_rejected():
    with pytest.raises(
        ValueError,
        match="calculation must be Percentage or Fixed Amount",
    ):
        make_tax_charge(calculation="Rate")


def test_negative_value_is_rejected():
    with pytest.raises(ValueError, match="value cannot be negative"):
        make_tax_charge(value=-1.0)


def test_invalid_scope_is_rejected():
    with pytest.raises(ValueError, match="scope must be Overall or Product"):
        make_tax_charge(scope="Category")


def test_product_scope_requires_product_id():
    with pytest.raises(ValueError, match="Product scope requires a product ID"):
        make_tax_charge(scope="Product", product_id=None)


def test_overall_scope_cannot_have_product_id():
    with pytest.raises(ValueError, match="Overall scope cannot have a product ID"):
        make_tax_charge(scope="Overall", product_id=1)


def test_empty_created_at_is_rejected():
    with pytest.raises(ValueError, match="creation timestamp cannot be empty"):
        make_tax_charge(created_at="   ")


def test_tax_code_supports_indirect_tax_codes():
    for code in ("GST", "CGST", "SGST", "IGST"):
        tax_charge = make_tax_charge(tax_code=code)
        assert tax_charge.tax_code == code


def test_charge_codes_are_reserved_for_charges():
    with pytest.raises(ValueError, match="must be charges"):
        make_tax_charge(tax_code="DELIVERY")
