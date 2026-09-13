from pathlib import Path

from application.services.customer_service import CustomerService
from application.services.product_service import ProductService
from application.services.supplier_service import SupplierService
from domain.entities.customer import Customer
from domain.entities.product import Product
from domain.entities.supplier import Supplier
from infrastructure.database.connection import get_connection
from infrastructure.database.initialization import initialize_database
from infrastructure.repositories.customer_repository import CustomerRepository
from infrastructure.repositories.product_repository import ProductRepository
from infrastructure.repositories.supplier_repository import SupplierRepository


def create_database(tmp_path: Path):
    database_path = tmp_path / "application_services.db"
    initialize_database(database_path)
    return get_connection(database_path)


def test_application_services_persist_and_retrieve_master_data(tmp_path):
    connection = create_database(tmp_path)

    try:
        product_service = ProductService(ProductRepository(connection))
        customer_service = CustomerService(CustomerRepository(connection))
        supplier_service = SupplierService(SupplierRepository(connection))

        product = Product(
            id=None,
            name="Integration Product",
            description="Product through application service",
            sku="SERVICE-001",
            price=750.0,
            quantity=20,
            created_at="2026-09-13T10:00:00",
        )

        customer = Customer(
            id=None,
            name="Integration Customer",
            phone="9876543210",
            email="customer@example.com",
            address="Delhi",
            created_at="2026-09-13T10:00:00",
        )

        supplier = Supplier(
            id=None,
            name="Integration Supplier",
            phone="9123456780",
            email="supplier@example.com",
            address="Mumbai",
            created_at="2026-09-13T10:00:00",
        )

        product_service.add_product(product)
        customer_service.add_customer(customer)
        supplier_service.add_supplier(supplier)

        assert product_service.get_product(product.id) == product
        assert customer_service.get_customer(customer.id) == customer
        assert supplier_service.get_supplier(supplier.id) == supplier

        assert product_service.get_products() == [product]
        assert customer_service.get_customers() == [customer]
        assert supplier_service.get_suppliers() == [supplier]
    finally:
        connection.close()
