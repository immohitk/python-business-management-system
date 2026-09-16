from pathlib import Path

from infrastructure.database.connection import get_connection
from infrastructure.database.initialization import initialize_database


def test_stock_movements_table_exists(tmp_path: Path):
    database_path = tmp_path / "test.db"

    initialize_database(database_path)
    connection = get_connection(database_path)

    try:
        row = connection.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
              AND name = 'stock_movements'
            """
        ).fetchone()

        assert row is not None
        assert row[0] == "stock_movements"
    finally:
        connection.close()


def test_stock_movements_table_has_product_foreign_key(tmp_path: Path):
    database_path = tmp_path / "test.db"

    initialize_database(database_path)
    connection = get_connection(database_path)

    try:
        foreign_keys = connection.execute(
            """
            PRAGMA foreign_key_list(stock_movements)
            """
        ).fetchall()

        assert any(
            row[2] == "products" and row[3] == "product_id"
            for row in foreign_keys
        )
    finally:
        connection.close()
