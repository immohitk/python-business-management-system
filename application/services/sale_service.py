from application.services.inventory_service import InventoryService
from domain.entities.sale import Sale
from domain.entities.sale_item import SaleItem
from infrastructure.database.transaction import transaction
from infrastructure.repositories.sale_repository import SaleRepository


class SaleService:
    """Application service for sale operations."""

    def __init__(
        self,
        sale_repository: SaleRepository,
        inventory_service: InventoryService,
    ) -> None:
        self.sale_repository = sale_repository
        self.inventory_service = inventory_service

    def create_sale(self, sale: Sale) -> Sale:
        with transaction(self.sale_repository.connection):
            sale.apply_calculated_total()

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
