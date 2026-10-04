from application.services.payment_balance_service import PaymentBalanceService
from domain.entities.sale_payment import SalePayment
from infrastructure.repositories.sale_payment_repository import SalePaymentRepository

from tests.integration.test_persistence import create_database


def test_payment_balance_with_persisted_payments(tmp_path) -> None:
    connection = create_database(tmp_path)

    try:
        repository = SalePaymentRepository(connection)

        payment_one = SalePayment(
            id=None,
            sale_id=1,
            payment_mode="UPI",
            amount=600.0,
            created_at="2026-10-04T21:00:00",
        )
        payment_two = SalePayment(
            id=None,
            sale_id=1,
            payment_mode="Cash",
            amount=200.0,
            created_at="2026-10-04T21:05:00",
        )

        repository.add(payment_one)
        repository.add(payment_two)

        payments = repository.get_by_sale_id(1)

        service = PaymentBalanceService()
        result = service.calculate(
            sale_total=1000.0,
            payments=payments,
        )

        assert result.paid_total == 800.0
        assert result.remaining_balance == 200.0
    finally:
        connection.close()