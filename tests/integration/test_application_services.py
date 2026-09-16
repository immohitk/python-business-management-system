import pytest
from pathlib import Path

from application.services.customer_service import CustomerService
from application.services.product_service import ProductService
from application.services.supplier_service import SupplierService
from application.services.inventory_service import InventoryService
from domain.entities.customer import Customer
from domain.entities.product import Product
from domain.entities.supplier import Supplier
from domain.entities.stock_movement import StockMovementType
from infrastructure.database.connection import get_connection
from infrastructure.database.initialization import initialize_database
from infrastructure.repositories.customer_repository import CustomerRepository
from infrastructure.repositories.product_repository import ProductRepository
from infrastructure.repositories.supplier_repository import SupplierRepository
from infrastructure.repositories.stock_movement_repository import (
    StockMovementRepository,
)


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


def test_inventory_service_persists_stock_operations(tmp_path):
    connection = create_database(tmp_path)

    try:
        product_repository = ProductRepository(connection)
        stock_movement_repository = StockMovementRepository(connection)
        inventory_service = InventoryService(
            product_repository,
            stock_movement_repository,
        )

        product = Product(
            id=None,
            name="Inventory Integration Product",
            description="Inventory service integration test",
            sku="INVENTORY-001",
            price=500.0,
            quantity=20,
            created_at="2026-09-16T10:00:00",
        )

        product_repository.add(product)

        inventory_service.stock_in(product.id, 5)
        inventory_service.adjust_stock(product.id, 12)
        inventory_service.stock_out(product.id, 4)

        result = product_repository.get_by_id(product.id)

        assert result is not None
        assert result.quantity == 8

        movements = stock_movement_repository.get_movements(product.id)

        assert len(movements) == 3

        assert movements[0].movement_type == StockMovementType.ADD
        assert movements[0].quantity == 5
        assert movements[0].resulting_stock == 25

        assert movements[1].movement_type == StockMovementType.ADJUST
        assert movements[1].quantity == 12
        assert movements[1].resulting_stock == 12

        assert movements[2].movement_type == StockMovementType.DEDUCT
        assert movements[2].quantity == 4
        assert movements[2].resulting_stock == 8
    finally:
        connection.close()


def test_inventory_service_rejects_invalid_stock_operations(tmp_path):
    connection = create_database(tmp_path)

    try:
        product_repository = ProductRepository(connection)
        stock_movement_repository = StockMovementRepository(connection)
        inventory_service = InventoryService(
            product_repository,
            stock_movement_repository,
        )

        product = Product(
            id=None,
            name="Inventory Validation Product",
            description=None,
            sku="INVENTORY-002",
            price=500.0,
            quantity=10,
            created_at="2026-09-16T10:00:00",
        )

        product_repository.add(product)

        with pytest.raises(
            ValueError,
            match="Stock addition amount must be greater than zero",
        ):
            inventory_service.stock_in(product.id, 0)

        with pytest.raises(
            ValueError,
            match="Stock quantity cannot be negative",
        ):
            inventory_service.adjust_stock(product.id, -1)

        with pytest.raises(
            ValueError,
            match="Stock deduction amount must be greater than zero",
        ):
            inventory_service.stock_out(product.id, 0)

        result = product_repository.get_by_id(product.id)

        assert result is not None
        assert result.quantity == 10
        assert stock_movement_repository.get_movements(product.id) == []
    finally:
        connection.close()


def test_inventory_service_rejects_insufficient_stock(tmp_path):
    connection = create_database(tmp_path)

    try:
        product_repository = ProductRepository(connection)
        stock_movement_repository = StockMovementRepository(connection)
        inventory_service = InventoryService(
            product_repository,
            stock_movement_repository,
        )

        product = Product(
            id=None,
            name="Insufficient Stock Product",
            description=None,
            sku="INVENTORY-003",
            price=500.0,
            quantity=10,
            created_at="2026-09-16T10:00:00",
        )

        product_repository.add(product)

        with pytest.raises(
            ValueError,
            match="Stock quantity cannot be negative",
        ):
            inventory_service.stock_out(product.id, 11)

        result = product_repository.get_by_id(product.id)

        assert result is not None
        assert result.quantity == 10
        assert stock_movement_repository.get_movements(product.id) == []
    finally:
        connection.close()
