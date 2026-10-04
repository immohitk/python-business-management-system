from dataclasses import dataclass

from domain.entities.sale_payment import SalePayment


@dataclass(frozen=True)
class PaymentBalanceResult:
    paid_total: float
    remaining_balance: float


class PaymentBalanceService:
    """Calculates paid total and remaining balance for a sale."""

    def calculate(
        self,
        sale_total: float,
        payments: list[SalePayment],
    ) -> PaymentBalanceResult:
        paid_total = sum(payment.amount for payment in payments)
        remaining_balance = sale_total - paid_total

        return PaymentBalanceResult(
            paid_total=paid_total,
            remaining_balance=remaining_balance,
        )