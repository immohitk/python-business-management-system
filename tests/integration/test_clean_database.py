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


def test_clean_database_can_be_initialized(tmp_path):
    database_path = tmp_path / "business.db"

    assert not database_path.exists()

    initialize_database(database_path)

    assert database_path.exists()
    assert database_path.is_file()


def test_clean_database_contains_expected_tables(tmp_path):
    database_path = tmp_path / "business.db"

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


def test_clean_database_contains_initial_schema_version(tmp_path):
    database_path = tmp_path / "business.db"

    initialize_database(database_path)

    connection = sqlite3.connect(database_path)

    try:
        result = connection.execute(
            "SELECT id, version FROM schema_version"
        ).fetchone()

        assert result == (1, "1")
    finally:
        connection.close()


def test_clean_database_can_be_reopened(tmp_path):
    database_path = tmp_path / "business.db"

    initialize_database(database_path)

    first_connection = sqlite3.connect(database_path)
    first_connection.close()

    second_connection = sqlite3.connect(database_path)

    try:
        result = second_connection.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table' AND name = 'products'
            """
        ).fetchone()

        assert result == ("products",)
    finally:
        second_connection.close()
