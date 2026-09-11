import sqlite3

from infrastructure.database.initialization import initialize_database


EXPECTED_TABLES = [
    "customers",
    "invoices",
    "products",
    "sale_items",
    "sales",
    "schema_version",
    "suppliers",
]


def test_initialize_database_creates_complete_schema(tmp_path):
    database_path = tmp_path / "test_business.db"

    initialize_database(database_path)

    connection = sqlite3.connect(database_path)

    try:
        rows = connection.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
            ORDER BY name
            """
        ).fetchall()

        tables = [row[0] for row in rows]

        assert tables == EXPECTED_TABLES
    finally:
        connection.close()


def test_initialize_database_creates_initial_schema_version(tmp_path):
    database_path = tmp_path / "test_business.db"

    initialize_database(database_path)

    connection = sqlite3.connect(database_path)

    try:
        result = connection.execute(
            "SELECT id, version FROM schema_version"
        ).fetchone()

        assert result == (1, "1")
    finally:
        connection.close()


def test_initialize_database_is_repeatable(tmp_path):
    database_path = tmp_path / "test_business.db"

    initialize_database(database_path)
    initialize_database(database_path)

    connection = sqlite3.connect(database_path)

    try:
        tables = connection.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
            ORDER BY name
            """
        ).fetchall()

        schema_versions = connection.execute(
            "SELECT id, version FROM schema_version"
        ).fetchall()

        assert [row[0] for row in tables] == EXPECTED_TABLES
        assert schema_versions == [(1, "1")]
    finally:
        connection.close()


def test_initialized_database_can_store_product_data(tmp_path):
    database_path = tmp_path / "test_business.db"

    initialize_database(database_path)

    connection = sqlite3.connect(database_path)

    try:
        connection.execute(
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
                "Test Product",
                "Integration test product",
                "TEST-001",
                100.0,
                10,
                "2026-01-01T00:00:00",
            ),
        )
        connection.commit()

        result = connection.execute(
            """
            SELECT name, sku, price, quantity
            FROM products
            WHERE sku = ?
            """,
            ("TEST-001",),
        ).fetchone()

        assert result == ("Test Product", "TEST-001", 100.0, 10)
    finally:
        connection.close()
