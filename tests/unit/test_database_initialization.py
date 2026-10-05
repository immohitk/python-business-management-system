import sqlite3

from infrastructure.database.config import DATABASE_PATH
from infrastructure.database.initialization import initialize_database


def test_initialize_database_creates_database_file():
    initialize_database()

    assert DATABASE_PATH.exists()
    assert DATABASE_PATH.is_file()


def test_initialize_database_creates_schema_version_table():
    initialize_database()

    connection = sqlite3.connect(DATABASE_PATH)

    try:
        result = connection.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table' AND name = 'schema_version'
            """
        ).fetchone()

        assert result == ("schema_version",)
    finally:
        connection.close()


def test_schema_version_contains_initial_version():
    initialize_database()

    connection = sqlite3.connect(DATABASE_PATH)

    try:
        result = connection.execute(
            "SELECT id, version FROM schema_version"
        ).fetchone()

        assert result == (1, "4")
    finally:
        connection.close()


def test_initialize_database_is_idempotent():
    initialize_database()
    initialize_database()

    connection = sqlite3.connect(DATABASE_PATH)

    try:
        rows = connection.execute(
            "SELECT id, version FROM schema_version"
        ).fetchall()

        assert rows == [(1, "4")]
    finally:
        connection.close()


def test_initialize_database_supports_custom_database_path(tmp_path):
    database_path = tmp_path / "test_business.db"

    initialize_database(database_path)

    assert database_path.exists()
    assert database_path.is_file()

    connection = sqlite3.connect(database_path)

    try:
        result = connection.execute(
            "SELECT id, version FROM schema_version"
        ).fetchone()

        assert result == (1, "4")
    finally:
        connection.close()


def test_migration_failure_restores_pre_migration_database(tmp_path, monkeypatch):
    database_path = tmp_path / "migration_failure.db"
    connection = sqlite3.connect(database_path)
    try:
        connection.executescript(
            """
            CREATE TABLE schema_version (id INTEGER PRIMARY KEY, version TEXT NOT NULL);
            INSERT INTO schema_version VALUES (1, '1');
            CREATE TABLE products (id INTEGER PRIMARY KEY, name TEXT NOT NULL, description TEXT,
                sku TEXT NOT NULL UNIQUE, price REAL NOT NULL, quantity INTEGER NOT NULL, created_at TEXT NOT NULL);
            INSERT INTO products VALUES (1, 'Legacy', 'Legacy data', 'LEG-ROLLBACK', 10, 4, '2026-01-01');
            """
        )
        connection.commit()
    finally:
        connection.close()

    def fail_customer_migration(_connection):
        raise RuntimeError("forced migration failure")

    monkeypatch.setattr("infrastructure.database.initialization._migrate_customer_columns", fail_customer_migration)

    import pytest
    with pytest.raises(RuntimeError, match="forced migration failure"):
        initialize_database(database_path)

    connection = sqlite3.connect(database_path)
    try:
        assert [row[1] for row in connection.execute("PRAGMA table_info(products)")] == [
            "id", "name", "description", "sku", "price", "quantity", "created_at"
        ]
        assert connection.execute("SELECT * FROM products").fetchone() == (
            1, "Legacy", "Legacy data", "LEG-ROLLBACK", 10.0, 4, "2026-01-01"
        )
        assert connection.execute("SELECT version FROM schema_version WHERE id=1").fetchone() == ("1",)
    finally:
        connection.close()
