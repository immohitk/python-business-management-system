import pytest

from domain.rules.inventory_rules import (
    validate_stock_addition,
    validate_stock_adjustment,
    validate_stock_deduction,
    validate_stock_quantity,
)


def test_stock_quantity_allows_zero():
    validate_stock_quantity(0)


def test_stock_quantity_allows_positive_value():
    validate_stock_quantity(10)


def test_stock_quantity_cannot_be_negative():
    with pytest.raises(
        ValueError,
        match="Stock quantity cannot be negative",
    ):
        validate_stock_quantity(-1)


def test_stock_addition_requires_positive_amount():
    with pytest.raises(
        ValueError,
        match="Stock addition amount must be greater than zero",
    ):
        validate_stock_addition(0)


def test_stock_addition_cannot_be_negative():
    with pytest.raises(
        ValueError,
        match="Stock addition amount must be greater than zero",
    ):
        validate_stock_addition(-5)


def test_stock_adjustment_allows_zero():
    validate_stock_adjustment(0)


def test_stock_adjustment_allows_positive_value():
    validate_stock_adjustment(15)


def test_stock_adjustment_cannot_be_negative():
    with pytest.raises(
        ValueError,
        match="Stock quantity cannot be negative",
    ):
        validate_stock_adjustment(-1)


def test_stock_deduction_requires_positive_amount():
    with pytest.raises(
        ValueError,
        match="Stock deduction amount must be greater than zero",
    ):
        validate_stock_deduction(0)


def test_stock_deduction_cannot_be_negative():
    with pytest.raises(
        ValueError,
        match="Stock deduction amount must be greater than zero",
    ):
        validate_stock_deduction(-3)
