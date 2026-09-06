import sqlite3

from infrastructure.database.connection import get_connection


def test_get_connection_returns_sqlite_connection():
    connection = get_connection()

    try:
        assert isinstance(connection, sqlite3.Connection)
    finally:
        connection.close()


def test_connection_can_execute_sql():
    connection = get_connection()

    try:
        cursor = connection.execute("SELECT 1")
        result = cursor.fetchone()

        assert result == (1,)
    finally:
        connection.close()


def test_get_connection_supports_custom_database_path(tmp_path):
    database_path = tmp_path / "test_business.db"

    connection = get_connection(database_path)

    try:
        assert isinstance(connection, sqlite3.Connection)
        assert database_path.exists()
        assert database_path.is_file()
    finally:
        connection.close()