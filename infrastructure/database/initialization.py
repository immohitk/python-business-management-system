from pathlib import Path

from infrastructure.database.connection import get_connection
from infrastructure.database.schema import get_schema_sql


def initialize_database(database_path: Path | None = None) -> None:
    connection = get_connection(database_path)

    try:
        connection.executescript(get_schema_sql())
        _migrate_product_columns(connection)
        connection.execute("UPDATE schema_version SET version='2' WHERE id=1")
        connection.commit()
    finally:
        connection.close()

def _migrate_product_columns(connection) -> None:
    """Add v2 product fields to databases created by the v1 schema.

    The migration is additive only: existing product rows keep their data and
    receive safe domain defaults for the new fields.
    """
    columns = {row[1] for row in connection.execute("PRAGMA table_info(products)")}
    additions = {
        "category_id": "INTEGER",
        "base_unit": "TEXT NOT NULL DEFAULT 'PCS'",
        "purchase_unit": "TEXT NOT NULL DEFAULT 'PCS'",
        "sales_unit": "TEXT NOT NULL DEFAULT 'PCS'",
        "purchase_to_base_conversion": "REAL NOT NULL DEFAULT 1.0",
        "sales_to_base_conversion": "REAL NOT NULL DEFAULT 1.0",
        "is_perishable": "INTEGER NOT NULL DEFAULT 0",
        "mrp_applicable": "INTEGER NOT NULL DEFAULT 0",
        "default_mrp": "REAL",
        "default_margin": "REAL NOT NULL DEFAULT 0.0",
        "min_margin": "REAL NOT NULL DEFAULT 0.0",
        "max_margin": "REAL NOT NULL DEFAULT 100.0",
        "default_tax_id": "INTEGER",
    }

    for column, definition in additions.items():
        if column not in columns:
            connection.execute(
                f"ALTER TABLE products ADD COLUMN {column} {definition}"
            )
