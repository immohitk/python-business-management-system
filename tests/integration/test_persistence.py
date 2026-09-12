from pathlib import Path

from domain.entities.customer import Customer
from domain.entities.invoice import Invoice
from domain.entities.product import Product
from domain.entities.sale import Sale
from domain.entities.sale_item import SaleItem
from domain.entities.supplier import Supplier
from infrastructure.database.connection import get_connection
from infrastructure.database.initialization import initialize_database
from infrastructure.repositories.customer_repository import CustomerRepository
from infrastructure.repositories.invoice_repository import InvoiceRepository
from infrastructure.repositories.product_repository import ProductRepository
from infrastructure.repositories.sale_repository import SaleRepository
from infrastructure.repositories.supplier_repository import SupplierRepository


def create_database(tmp_path: Path):
    database_path = tmp_path / "integration.db"
    initialize_database(database_path)
    return get_connection(database_path)


def test_product_customer_supplier_persistence(tmp_path):
    connection = create_database(tmp_path)

    try:
        product_repository = ProductRepository(connection)
        customer_repository = CustomerRepository(connection)
        supplier_repository = SupplierRepository(connection)

        product = Product(
            id=None,
            name="Interior Paint",
            description="White wall paint",
            sku="PAINT-INT-001",
            price=850.0,
            quantity=25,
            created_at="2026-09-07T20:00:00",
        )

        customer = Customer(
            id=None,
            name="Test Customer",
            phone="9876543210",
            email="customer@example.com",
            address="Delhi",
            created_at="2026-09-07T20:00:00",
        )

        supplier = Supplier(
            id=None,
            name="Test Supplier",
            phone="9123456780",
            email="supplier@example.com",
            address="Mumbai",
            created_at="2026-09-07T20:00:00",
        )

        product_repository.add(product)
        customer_repository.add(customer)
        supplier_repository.add(supplier)

        assert product_repository.get_by_id(product.id) == product
        assert customer_repository.get_by_id(customer.id) == customer
        assert supplier_repository.get_by_id(supplier.id) == supplier
    finally:
        connection.close()


def test_sale_sale_item_and_invoice_persistence(tmp_path):
    connection = create_database(tmp_path)

    try:
        product_repository = ProductRepository(connection)
        customer_repository = CustomerRepository(connection)
        sale_repository = SaleRepository(connection)
        invoice_repository = InvoiceRepository(connection)

        product = Product(
            id=None,
            name="Exterior Paint",
            description="Weather resistant paint",
            sku="PAINT-EXT-001",
            price=1200.0,
            quantity=15,
            created_at="2026-09-07T20:00:00",
        )

        customer = Customer(
            id=None,
            name="Integration Customer",
            phone="9876543210",
            email="integration@example.com",
            address="Delhi",
            created_at="2026-09-07T20:00:00",
        )

        product_repository.add(product)
        customer_repository.add(customer)

        sale = Sale(
            id=None,
            customer_id=customer.id,
            sale_date="2026-09-07",
            total_amount=2400.0,
            created_at="2026-09-07T20:00:00",
        )

        sale_repository.add(sale)

        sale_item = SaleItem(
            id=None,
            sale_id=sale.id,
            product_id=product.id,
            quantity=2,
            unit_price=1200.0,
        )

        sale_repository.add_item(sale_item)

        invoice = Invoice(
            id=None,
            sale_id=sale.id,
            invoice_number="INV-INT-001",
            invoice_date="2026-09-07",
            total_amount=2400.0,
            created_at="2026-09-07T20:00:00",
        )

        invoice_repository.add(invoice)

        stored_sale = sale_repository.get_by_id(sale.id)
        stored_items = sale_repository.get_items(sale.id)
        stored_invoice = invoice_repository.get_by_id(invoice.id)

        assert stored_sale == sale
        assert stored_items == [sale_item]
        assert stored_invoice == invoice
        assert stored_sale.customer_id == customer.id
        assert stored_items[0].product_id == product.id
        assert stored_invoice.sale_id == sale.id
    finally:
        connection.close()


def test_master_data_survives_connection_reopen(tmp_path):
    database_path = tmp_path / "integration.db"
    initialize_database(database_path)

    connection = get_connection(database_path)

    product = Product(
        id=None,
        name="Reopen Product",
        description="Persistence test product",
        sku="REOPEN-001",
        price=500.0,
        quantity=10,
        created_at="2026-09-11T16:00:00",
    )

    customer = Customer(
        id=None,
        name="Reopen Customer",
        phone="9000000001",
        email="reopen@example.com",
        address="Delhi",
        created_at="2026-09-11T16:00:00",
    )

    supplier = Supplier(
        id=None,
        name="Reopen Supplier",
        phone="9000000002",
        email="supplier-reopen@example.com",
        address="Mumbai",
        created_at="2026-09-11T16:00:00",
    )

    try:
        ProductRepository(connection).add(product)
        CustomerRepository(connection).add(customer)
        SupplierRepository(connection).add(supplier)
    finally:
        connection.close()

    reopened_connection = get_connection(database_path)

    try:
        product_repository = ProductRepository(reopened_connection)
        customer_repository = CustomerRepository(reopened_connection)
        supplier_repository = SupplierRepository(reopened_connection)

        assert product_repository.get_by_id(product.id) == product
        assert customer_repository.get_by_id(customer.id) == customer
        assert supplier_repository.get_by_id(supplier.id) == supplier
    finally:
        reopened_connection.close()


def test_sale_data_survives_connection_reopen(tmp_path):
    database_path = tmp_path / "integration.db"
    initialize_database(database_path)

    connection = get_connection(database_path)

    product = Product(
        id=None,
        name="Reopen Sale Product",
        description="Product for sale persistence",
        sku="REOPEN-SALE-001",
        price=750.0,
        quantity=20,
        created_at="2026-09-11T16:00:00",
    )

    customer = Customer(
        id=None,
        name="Reopen Sale Customer",
        phone="9000000010",
        email="sale-reopen@example.com",
        address="Bengaluru",
        created_at="2026-09-11T16:00:00",
    )

    try:
        product_repository = ProductRepository(connection)
        customer_repository = CustomerRepository(connection)
        sale_repository = SaleRepository(connection)
        invoice_repository = InvoiceRepository(connection)

        product_repository.add(product)
        customer_repository.add(customer)

        sale = Sale(
            id=None,
            customer_id=customer.id,
            sale_date="2026-09-11",
            total_amount=1500.0,
            created_at="2026-09-11T16:00:00",
        )
        sale_repository.add(sale)

        sale_item = SaleItem(
            id=None,
            sale_id=sale.id,
            product_id=product.id,
            quantity=2,
            unit_price=750.0,
        )
        sale_repository.add_item(sale_item)

        invoice = Invoice(
            id=None,
            sale_id=sale.id,
            invoice_number="INV-REOPEN-001",
            invoice_date="2026-09-11",
            total_amount=1500.0,
            created_at="2026-09-11T16:00:00",
        )
        invoice_repository.add(invoice)
    finally:
        connection.close()

    reopened_connection = get_connection(database_path)

    try:
        sale_repository = SaleRepository(reopened_connection)
        invoice_repository = InvoiceRepository(reopened_connection)

        stored_sale = sale_repository.get_by_id(sale.id)
        stored_items = sale_repository.get_items(sale.id)
        stored_invoice = invoice_repository.get_by_id(invoice.id)

        assert stored_sale == sale
        assert stored_items == [sale_item]
        assert stored_invoice == invoice
        assert stored_sale.customer_id == customer.id
        assert stored_items[0].product_id == product.id
        assert stored_invoice.sale_id == sale.id
    finally:
        reopened_connection.close()


def test_products_survive_connection_reopen_and_list_in_order(tmp_path):
    database_path = tmp_path / "integration.db"
    initialize_database(database_path)

    connection = get_connection(database_path)

    first_product = Product(
        id=None,
        name="Wall Paint",
        description="Interior wall paint",
        sku="WALL-001",
        price=850.0,
        quantity=25,
        created_at="2026-09-12T10:00:00",
    )

    second_product = Product(
        id=None,
        name="Paint Brush",
        description="Medium paint brush",
        sku="BRUSH-001",
        price=120.0,
        quantity=15,
        created_at="2026-09-12T10:00:00",
    )

    try:
        repository = ProductRepository(connection)

        repository.add(first_product)
        repository.add(second_product)
    finally:
        connection.close()

    reopened_connection = get_connection(database_path)

    try:
        repository = ProductRepository(reopened_connection)

        result = repository.get_all()

        assert result == [first_product, second_product]
    finally:
        reopened_connection.close()
