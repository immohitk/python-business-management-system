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

        assert result == (1, "1")
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

        assert rows == [(1, "1")]
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

        assert result == (1, "1")
    finally:
        connection.close()