from application.services.customer_service import CustomerService
from application.services.inventory_service import InventoryService
from application.services.invoice_presentation_service import (
    InvoicePresentationService,
)
from application.services.invoice_service import InvoiceService
from application.services.product_service import ProductService
from application.services.reporting_service import ReportingService
from application.services.sale_invoice_service import SaleInvoiceService
from application.services.sale_service import SaleService
from application.services.supplier_service import SupplierService
from infrastructure.database.connection import get_connection
from infrastructure.repositories.customer_repository import CustomerRepository
from infrastructure.repositories.invoice_repository import InvoiceRepository
from infrastructure.repositories.product_repository import ProductRepository
from infrastructure.repositories.reporting_repository import ReportingRepository
from infrastructure.repositories.sale_repository import SaleRepository
from infrastructure.repositories.stock_movement_repository import (
    StockMovementRepository,
)
from infrastructure.repositories.supplier_repository import SupplierRepository


class CLIContext:
    def __init__(self) -> None:
        self.connection = get_connection()

        product_repository = ProductRepository(self.connection)
        customer_repository = CustomerRepository(self.connection)
        supplier_repository = SupplierRepository(self.connection)
        sale_repository = SaleRepository(self.connection)
        invoice_repository = InvoiceRepository(self.connection)
        stock_movement_repository = StockMovementRepository(self.connection)
        reporting_repository = ReportingRepository(self.connection)

        self.product_service = ProductService(product_repository)
        self.customer_service = CustomerService(customer_repository)
        self.supplier_service = SupplierService(supplier_repository)

        self.inventory_service = InventoryService(
            product_repository,
            stock_movement_repository,
        )

        self.sale_service = SaleService(
            sale_repository,
            self.inventory_service,
        )

        self.invoice_service = InvoiceService(invoice_repository)

        self.sale_invoice_service = SaleInvoiceService(
            sale_repository=sale_repository,
            invoice_service=self.invoice_service,
        )

        self.invoice_presentation_service = InvoicePresentationService(
            invoice_repository=invoice_repository,
            sale_repository=sale_repository,
            customer_repository=customer_repository,
            product_repository=product_repository,
        )

        self.reporting_service = ReportingService(reporting_repository)

    def close(self) -> None:
        self.connection.close()
