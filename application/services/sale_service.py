from application.services.inventory_service import InventoryService
from application.services.payment_balance_service import PaymentBalanceService
from application.services.sale_calculation_service import SaleCalculationService
from application.services.sale_payment_service import SalePaymentService
from domain.entities.sale import Sale
from domain.entities.sale_item import SaleItem
from domain.entities.sale_payment import SalePayment
from infrastructure.database.transaction import transaction
from infrastructure.repositories.sale_repository import SaleRepository
from infrastructure.repositories.tax_charge_repository import TaxChargeRepository


class SaleService:
    """Application service for sale operations."""

    def __init__(
        self,
        sale_repository: SaleRepository,
        inventory_service: InventoryService,
        tax_charge_repository: TaxChargeRepository,
        sale_calculation_service: SaleCalculationService,
        sale_payment_service: SalePaymentService,
        payment_balance_service: PaymentBalanceService,
    ) -> None:
        self.sale_repository = sale_repository
        self.inventory_service = inventory_service
        self.tax_charge_repository = tax_charge_repository
        self.sale_calculation_service = sale_calculation_service
        self.sale_payment_service = sale_payment_service
        self.payment_balance_service = payment_balance_service

    def create_sale(
        self,
        sale: Sale,
        payments: list[tuple[str, float]] | None = None,
    ) -> Sale:
        with transaction(self.sale_repository.connection):
            tax_charges = self.tax_charge_repository.get_all()

            calculation = self.sale_calculation_service.calculate(
                sale=sale,
                tax_charges=tax_charges,
            )

            sale.total_amount = calculation.final_total

            self.sale_repository.add(sale)

            # Snapshot the exact tax/charge configuration used for this sale.
            # Later configuration edits therefore cannot rewrite history.
            for tax_charge in tax_charges:
                if not tax_charge.is_active:
                    continue
                if tax_charge.scope == "Overall":
                    amount = self.sale_calculation_service.tax_charge_calculator.calculate(
                        tax_charge, calculation.subtotal
                    )
                    if amount:
                        self.tax_charge_repository.snapshot_for_sale(
                            sale.id, tax_charge, amount, sale.created_at
                        )
                else:
                    for line in sale.lines:
                        if tax_charge.product_id != line.product_id:
                            continue
                        amount = self.sale_calculation_service.tax_charge_calculator.calculate(
                            tax_charge, line.subtotal, line.product_id
                        )
                        if amount:
                            self.tax_charge_repository.snapshot_for_sale(
                                sale.id, tax_charge, amount, sale.created_at
                            )

            for line in sale.lines:
                sale_item = SaleItem(
                    id=None,
                    sale_id=sale.id,
                    product_id=line.product_id,
                    quantity=line.quantity,
                    unit_price=line.unit_price,
                )
                self.sale_repository.add_item(sale_item)

                self.inventory_service.stock_out(
                    product_id=line.product_id,
                    amount=line.quantity,
                    created_at=sale.created_at,
                )

            payment_entries = [
                SalePayment(
                    id=None,
                    sale_id=sale.id,
                    payment_mode=payment_mode,
                    amount=amount,
                    created_at=sale.created_at,
                )
                for payment_mode, amount in payments or []
            ]

            payment_balance = self.payment_balance_service.calculate(
                sale_total=sale.total_amount,
                payments=payment_entries,
            )

            if payment_balance.remaining_balance < 0:
                raise ValueError("Payment amount cannot exceed sale total.")

            for payment in payment_entries:
                self.sale_payment_service.add_payment(payment)

        return sale

    def get_sales(self) -> list[Sale]:
        return self.sale_repository.get_all()