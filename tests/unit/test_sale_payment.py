import pytest

from domain.entities.sale_payment import SalePayment


def make_payment(**overrides) -> SalePayment:
    values = {
        "id": None,
        "sale_id": 1,
        "payment_mode": "Cash",
        "amount": 500.0,
        "created_at": "2026-10-04T01:00:00",
    }
    values.update(overrides)
    return SalePayment(**values)


def test_creates_valid_sale_payment() -> None:
    payment = make_payment()

    assert payment.id is None
    assert payment.sale_id == 1
    assert payment.payment_mode == "Cash"
    assert payment.amount == 500.0


@pytest.mark.parametrize(
    "payment_mode",
    ["Cash", "UPI", "Card", "Bank Transfer", "Other"],
)
def test_accepts_supported_payment_modes(payment_mode: str) -> None:
    payment = make_payment(payment_mode=payment_mode)

    assert payment.payment_mode == payment_mode


def test_rejects_invalid_sale_id() -> None:
    with pytest.raises(ValueError, match="Sale ID must be greater than zero"):
        make_payment(sale_id=0)


def test_rejects_invalid_payment_mode() -> None:
    with pytest.raises(ValueError, match="Payment mode must be"):
        make_payment(payment_mode="Cheque")


def test_rejects_zero_payment_amount() -> None:
    with pytest.raises(
        ValueError,
        match="Payment amount must be greater than zero",
    ):
        make_payment(amount=0)


def test_rejects_negative_payment_amount() -> None:
    with pytest.raises(
        ValueError,
        match="Payment amount must be greater than zero",
    ):
        make_payment(amount=-100)


def test_rejects_empty_created_at() -> None:
    with pytest.raises(
        ValueError,
        match="Payment creation timestamp cannot be empty",
    ):
        make_payment(created_at="   ")
