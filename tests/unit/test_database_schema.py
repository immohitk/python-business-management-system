import sqlite3

from infrastructure.database.initialization import initialize_database
from infrastructure.database.schema import get_schema_sql


def test_schema_sql_is_not_empty():
    assert get_schema_sql().strip()


def test_schema_sql_defines_schema_version_table():
    schema_sql = get_schema_sql()

    assert "CREATE TABLE IF NOT EXISTS schema_version" in schema_sql


def test_schema_sql_defines_version_column():
    schema_sql = get_schema_sql()

    assert "version TEXT NOT NULL" in schema_sql


def test_products_table_has_expected_columns(tmp_path):
    database_path = tmp_path / "test_business.db"

    initialize_database(database_path)

    connection = sqlite3.connect(database_path)

    try:
        columns = connection.execute(
            "PRAGMA table_info(products)"
        ).fetchall()

        column_names = [column[1] for column in columns]

        assert column_names == [
            "id",
            "name",
            "description",
            "sku",
            "price",
            "quantity",
            "created_at",
        ]
    finally:
        connection.close()


def test_products_table_has_expected_constraints(tmp_path):
    database_path = tmp_path / "test_business.db"

    initialize_database(database_path)

    connection = sqlite3.connect(database_path)

    try:
        columns = connection.execute(
            "PRAGMA table_info(products)"
        ).fetchall()

        column_map = {column[1]: column for column in columns}

        assert column_map["id"][5] == 1
        assert column_map["name"][3] == 1
        assert column_map["sku"][3] == 1
        assert column_map["price"][3] == 1
        assert column_map["quantity"][3] == 1
        assert column_map["created_at"][3] == 1

        indexes = connection.execute(
            "PRAGMA index_list(products)"
        ).fetchall()

        unique_indexes = [
            index for index in indexes if index[2] == 1
        ]

        assert unique_indexes
    finally:
        connection.close()


def test_customers_table_has_expected_columns(tmp_path):
    database_path = tmp_path / "test_business.db"

    initialize_database(database_path)

    connection = sqlite3.connect(database_path)

    try:
        columns = connection.execute(
            "PRAGMA table_info(customers)"
        ).fetchall()

        column_names = [column[1] for column in columns]

        assert column_names == [
            "id",
            "name",
            "phone",
            "email",
            "address",
            "created_at",
        ]
    finally:
        connection.close()


def test_customers_table_has_expected_constraints(tmp_path):
    database_path = tmp_path / "test_business.db"

    initialize_database(database_path)

    connection = sqlite3.connect(database_path)

    try:
        columns = connection.execute(
            "PRAGMA table_info(customers)"
        ).fetchall()

        column_map = {column[1]: column for column in columns}

        assert column_map["id"][5] == 1
        assert column_map["name"][3] == 1
        assert column_map["created_at"][3] == 1

        assert column_map["phone"][3] == 0
        assert column_map["email"][3] == 0
        assert column_map["address"][3] == 0
    finally:
        connection.close()


def test_suppliers_table_has_expected_columns(tmp_path):
    database_path = tmp_path / "test_business.db"

    initialize_database(database_path)

    connection = sqlite3.connect(database_path)

    try:
        columns = connection.execute(
            "PRAGMA table_info(suppliers)"
        ).fetchall()

        column_names = [column[1] for column in columns]

        assert column_names == [
            "id",
            "name",
            "phone",
            "email",
            "address",
            "created_at",
        ]
    finally:
        connection.close()


def test_suppliers_table_has_expected_constraints(tmp_path):
    database_path = tmp_path / "test_business.db"

    initialize_database(database_path)

    connection = sqlite3.connect(database_path)

    try:
        columns = connection.execute(
            "PRAGMA table_info(suppliers)"
        ).fetchall()

        column_map = {column[1]: column for column in columns}

        assert column_map["id"][5] == 1
        assert column_map["name"][3] == 1
        assert column_map["created_at"][3] == 1

        assert column_map["phone"][3] == 0
        assert column_map["email"][3] == 0
        assert column_map["address"][3] == 0
    finally:
        connection.close()


def test_sales_table_has_expected_columns(tmp_path):
    database_path = tmp_path / "test_business.db"

    initialize_database(database_path)

    connection = sqlite3.connect(database_path)

    try:
        columns = connection.execute(
            "PRAGMA table_info(sales)"
        ).fetchall()

        column_names = [column[1] for column in columns]

        assert column_names == [
            "id",
            "customer_id",
            "sale_date",
            "total_amount",
            "created_at",
        ]
    finally:
        connection.close()


def test_sale_items_table_has_expected_columns(tmp_path):
    database_path = tmp_path / "test_business.db"

    initialize_database(database_path)

    connection = sqlite3.connect(database_path)

    try:
        columns = connection.execute(
            "PRAGMA table_info(sale_items)"
        ).fetchall()

        column_names = [column[1] for column in columns]

        assert column_names == [
            "id",
            "sale_id",
            "product_id",
            "quantity",
            "unit_price",
        ]
    finally:
        connection.close()


def test_sales_and_sale_items_have_expected_foreign_keys(tmp_path):
    database_path = tmp_path / "test_business.db"

    initialize_database(database_path)

    connection = sqlite3.connect(database_path)

    try:
        sales_foreign_keys = connection.execute(
            "PRAGMA foreign_key_list(sales)"
        ).fetchall()

        sale_items_foreign_keys = connection.execute(
            "PRAGMA foreign_key_list(sale_items)"
        ).fetchall()

        sales_relationships = {
            (foreign_key[3], foreign_key[2], foreign_key[4])
            for foreign_key in sales_foreign_keys
        }

        sale_items_relationships = {
            (foreign_key[3], foreign_key[2], foreign_key[4])
            for foreign_key in sale_items_foreign_keys
        }

        assert ("customer_id", "customers", "id") in sales_relationships

        assert ("sale_id", "sales", "id") in sale_items_relationships
        assert ("product_id", "products", "id") in sale_items_relationships
    finally:
        connection.close()
