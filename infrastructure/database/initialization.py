from pathlib import Path

from infrastructure.database.connection import get_connection
from infrastructure.database.schema import get_schema_sql


def initialize_database(database_path: Path | None = None) -> None:
    connection = get_connection(database_path)

    try:
        connection.executescript(get_schema_sql())
        _migrate_product_columns(connection)
        _migrate_customer_columns(connection)
        _migrate_tax_charge_columns(connection)
        _migrate_supplier_product_table(connection)
        _seed_units(connection)
        connection.execute("UPDATE schema_version SET version='4' WHERE id=1")
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


def _seed_units(connection) -> None:
    """Seed the standard v2 unit catalog without overwriting user changes."""
    units = [
        ("PCS", "Piece", "COUNT", 1.0),
        ("DOZEN", "Dozen", "COUNT", 12.0),
        ("GRAM", "Gram", "MASS", 1.0),
        ("KG", "Kilogram", "MASS", 1000.0),
        ("ML", "Millilitre", "VOLUME", 1.0),
        ("LITRE", "Litre", "VOLUME", 1000.0),
        # Package units intentionally have separate dimensions. Their actual
        # pack size is product-specific and must not be guessed globally.
        ("CARTON", "Carton", "CARTON", 1.0),
        ("BOX", "Box", "BOX", 1.0),
        ("PACK", "Pack", "PACK", 1.0),
    ]
    connection.executemany(
        """
        INSERT OR IGNORE INTO units (code, name, dimension, to_base_factor)
        VALUES (?, ?, ?, ?)
        """,
        units,
    )


def _migrate_customer_columns(connection) -> None:
    """Add v2 customer fields without changing existing customer data."""
    columns = {row[1] for row in connection.execute("PRAGMA table_info(customers)")}
    additions = {
        "city": "TEXT",
        "state": "TEXT",
        "pincode": "TEXT",
        "status": "TEXT NOT NULL DEFAULT 'ACTIVE'",
    }

    for column, definition in additions.items():
        if column not in columns:
            connection.execute(
                f"ALTER TABLE customers ADD COLUMN {column} {definition}"
            )


def _migrate_tax_charge_columns(connection) -> None:
    """Add v2 tax/charge metadata and snapshot storage additively."""
    columns = {row[1] for row in connection.execute("PRAGMA table_info(taxes_charges)")}
    additions = {
        "tax_code": "TEXT NOT NULL DEFAULT 'OTHER'",
        "is_default": "INTEGER NOT NULL DEFAULT 0",
    }
    for column, definition in additions.items():
        if column not in columns:
            connection.execute(f"ALTER TABLE taxes_charges ADD COLUMN {column} {definition}")

    connection.execute("""
        CREATE TABLE IF NOT EXISTS sale_tax_charge_snapshots (
            id INTEGER PRIMARY KEY,
            sale_id INTEGER NOT NULL,
            tax_charge_id INTEGER,
            name TEXT NOT NULL,
            type TEXT NOT NULL,
            calculation TEXT NOT NULL,
            value REAL NOT NULL,
            scope TEXT NOT NULL,
            product_id INTEGER,
            amount REAL NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY (sale_id) REFERENCES sales(id),
            FOREIGN KEY (tax_charge_id) REFERENCES taxes_charges(id)
        )
    """)


def _migrate_supplier_product_table(connection) -> None:
    """Create the v2 supplier-product many-to-many relationship additively."""
    connection.execute("""
        CREATE TABLE IF NOT EXISTS supplier_products (
            supplier_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            PRIMARY KEY (supplier_id, product_id),
            FOREIGN KEY (supplier_id) REFERENCES suppliers(id) ON DELETE CASCADE,
            FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
        )
    """)
