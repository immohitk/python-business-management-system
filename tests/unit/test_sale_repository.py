from pathlib import Path

from domain.entities.sale import Sale
from domain.entities.sale_item import SaleItem
from infrastructure.database.connection import get_connection
from infrastructure.database.initialization import initialize_database
from infrastructure.repositories.sale_repository import SaleRepository


def create_repository(tmp_path: Path) -> tuple[SaleRepository, object]:
    database_path = tmp_path / "test.db"
    initialize_database(database_path)
    connection = get_connection(database_path)

    return SaleRepository(connection), connection


def create_customer(connection) -> int:
    cursor = connection.execute(
        """
        INSERT INTO customers (
            name,
            phone,
            email,
            address,
            created_at
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            "Test Customer",
            "9876543210",
            "customer@example.com",
            "Delhi",
            "2026-09-07T20:00:00",
        ),
    )
    connection.commit()

    return cursor.lastrowid


def create_product(connection) -> int:
    cursor = connection.execute(
        """
        INSERT INTO products (
            name,
            description,
            sku,
            price,
            quantity,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            "Test Paint",
            "Test product",
            "TEST-PAINT-001",
            450.0,
            20,
            "2026-09-07T20:00:00",
        ),
    )
    connection.commit()

    return cursor.lastrowid


def create_sale(connection) -> Sale:
    customer_id = create_customer(connection)

    return Sale(
        id=None,
        customer_id=customer_id,
        sale_date="2026-09-07",
        total_amount=900.0,
        created_at="2026-09-07T20:00:00",
    )


def test_add_sale(tmp_path):
    repository, connection = create_repository(tmp_path)

    try:
        sale = create_sale(connection)

        repository.add(sale)

        assert sale.id is not None
        assert sale.id > 0
    finally:
        connection.close()


def test_get_sale_by_id(tmp_path):
    repository, connection = create_repository(tmp_path)

    try:
        sale = create_sale(connection)
        repository.add(sale)

        result = repository.get_by_id(sale.id)

        assert result == sale
    finally:
        connection.close()


def test_get_sale_by_id_returns_none_for_missing_sale(tmp_path):
    repository, connection = create_repository(tmp_path)

    try:
        result = repository.get_by_id(999)

        assert result is None
    finally:
        connection.close()


def test_get_all_sales(tmp_path):
    repository, connection = create_repository(tmp_path)

    try:
        first_sale = create_sale(connection)
        second_sale = create_sale(connection)

        repository.add(first_sale)
        repository.add(second_sale)

        result = repository.get_all()

        assert result == [first_sale, second_sale]
    finally:
        connection.close()


def test_delete_sale(tmp_path):
    repository, connection = create_repository(tmp_path)

    try:
        sale = create_sale(connection)
        repository.add(sale)

        repository.delete(sale.id)

        assert repository.get_by_id(sale.id) is None
    finally:
        connection.close()


def test_add_sale_item(tmp_path):
    repository, connection = create_repository(tmp_path)

    try:
        sale = create_sale(connection)
        repository.add(sale)

        product_id = create_product(connection)

        sale_item = SaleItem(
            id=None,
            sale_id=sale.id,
            product_id=product_id,
            quantity=2,
            unit_price=450.0,
        )

        repository.add_item(sale_item)

        assert sale_item.id is not None
        assert sale_item.id > 0
    finally:
        connection.close()


def test_get_sale_items(tmp_path):
    repository, connection = create_repository(tmp_path)

    try:
        sale = create_sale(connection)
        repository.add(sale)

        product_id = create_product(connection)

        first_item = SaleItem(
            id=None,
            sale_id=sale.id,
            product_id=product_id,
            quantity=2,
            unit_price=450.0,
        )

        second_item = SaleItem(
            id=None,
            sale_id=sale.id,
            product_id=product_id,
            quantity=1,
            unit_price=300.0,
        )

        repository.add_item(first_item)
        repository.add_item(second_item)

        result = repository.get_items(sale.id)

        assert result == [first_item, second_item]
    finally:
        connection.close()