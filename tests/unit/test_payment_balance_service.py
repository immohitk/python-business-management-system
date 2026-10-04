from application.services.payment_balance_service import PaymentBalanceService
from domain.entities.sale_payment import SalePayment


def create_payment(
    amount: float,
    payment_mode: str = "UPI",
) -> SalePayment:
    return SalePayment(
        id=None,
        sale_id=1,
        payment_mode=payment_mode,
        amount=amount,
        created_at="2026-10-04T21:00:00",
    )


def test_calculates_paid_total_and_remaining_balance() -> None:
    service = PaymentBalanceService()
    payments = [
        create_payment(600.0, "UPI"),
        create_payment(200.0, "Cash"),
    ]

    result = service.calculate(
        sale_total=1000.0,
        payments=payments,
    )

    assert result.paid_total == 800.0
    assert result.remaining_balance == 200.0


def test_returns_full_remaining_balance_when_no_payments_exist() -> None:
    service = PaymentBalanceService()

    result = service.calculate(
        sale_total=1000.0,
        payments=[],
    )

    assert result.paid_total == 0.0
    assert result.remaining_balance == 1000.0


def test_returns_zero_remaining_balance_when_fully_paid() -> None:
    service = PaymentBalanceService()
    payments = [create_payment(1000.0)]

    result = service.calculate(
        sale_total=1000.0,
        payments=payments,
    )

    assert result.paid_total == 1000.0
    assert result.remaining_balance == 0.0


def test_supports_multiple_payment_modes() -> None:
    service = PaymentBalanceService()
    payments = [
        create_payment(300.0, "Cash"),
        create_payment(250.0, "UPI"),
        create_payment(450.0, "Card"),
    ]

    result = service.calculate(
        sale_total=1000.0,
        payments=payments,
    )

    assert result.paid_total == 1000.0
    assert result.remaining_balance == 0.0


def test_remaining_balance_can_be_negative_for_overpayment() -> None:
    service = PaymentBalanceService()
    payments = [create_payment(1200.0)]

    result = service.calculate(
        sale_total=1000.0,
        payments=payments,
    )

    assert result.paid_total == 1200.0
    assert result.remaining_balance == -200.0