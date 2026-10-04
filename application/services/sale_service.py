from application.services.inventory_service import InventoryService
from application.services.sale_calculation_service import SaleCalculationService
from domain.entities.sale import Sale
from domain.entities.sale_item import SaleItem
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
    ) -> None:
        self.sale_repository = sale_repository
        self.inventory_service = inventory_service
        self.tax_charge_repository = tax_charge_repository
        self.sale_calculation_service = sale_calculation_service

    def create_sale(self, sale: Sale) -> Sale:
        with transaction(self.sale_repository.connection):
            tax_charges = self.tax_charge_repository.get_all()

            calculation = self.sale_calculation_service.calculate(
                sale=sale,
                tax_charges=tax_charges,
            )

            sale.total_amount = calculation.final_total

            self.sale_repository.add(sale)

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

        return sale

    def get_sales(self) -> list[Sale]:
        return self.sale_repository.get_all()