from domain.entities.sale_payment import SalePayment
from infrastructure.repositories.sale_payment_repository import SalePaymentRepository


class SalePaymentService:
    """Application service for SalePayment operations."""

    def __init__(self, repository: SalePaymentRepository) -> None:
        self.repository = repository

    def add_payment(self, payment: SalePayment) -> None:
        self.repository.add(payment)

    def get_payment(self, payment_id: int) -> SalePayment | None:
        return self.repository.get_by_id(payment_id)

    def get_payments_for_sale(self, sale_id: int) -> list[SalePayment]:
        return self.repository.get_by_sale_id(sale_id)

    def get_payments(self) -> list[SalePayment]:
        return self.repository.get_all()

    def delete_payment(self, payment_id: int) -> None:
        self.repository.delete(payment_id)