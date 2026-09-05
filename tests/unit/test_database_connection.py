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