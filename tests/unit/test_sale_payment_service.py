from unittest.mock import Mock

from application.services.sale_payment_service import SalePaymentService
from domain.entities.sale_payment import SalePayment


def create_payment() -> SalePayment:
    return SalePayment(
        id=1,
        sale_id=10,
        payment_mode="UPI",
        amount=600.0,
        created_at="2026-10-04T01:10:00",
    )


def test_add_payment() -> None:
    repository = Mock()
    service = SalePaymentService(repository)
    payment = create_payment()

    service.add_payment(payment)

    repository.add.assert_called_once_with(payment)


def test_get_payment() -> None:
    repository = Mock()
    payment = create_payment()
    repository.get_by_id.return_value = payment
    service = SalePaymentService(repository)

    result = service.get_payment(1)

    assert result == payment
    repository.get_by_id.assert_called_once_with(1)


def test_get_payments_for_sale() -> None:
    repository = Mock()
    payment = create_payment()
    repository.get_by_sale_id.return_value = [payment]
    service = SalePaymentService(repository)

    result = service.get_payments_for_sale(10)

    assert result == [payment]
    repository.get_by_sale_id.assert_called_once_with(10)


def test_get_payments() -> None:
    repository = Mock()
    payment = create_payment()
    repository.get_all.return_value = [payment]
    service = SalePaymentService(repository)

    result = service.get_payments()

    assert result == [payment]
    repository.get_all.assert_called_once_with()


def test_delete_payment() -> None:
    repository = Mock()
    service = SalePaymentService(repository)

    service.delete_payment(1)

    repository.delete.assert_called_once_with(1)