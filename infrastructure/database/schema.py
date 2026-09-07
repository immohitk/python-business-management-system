SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS schema_version (
    id INTEGER PRIMARY KEY,
    version TEXT NOT NULL
);

INSERT OR IGNORE INTO schema_version (id, version)
VALUES (1, '1');

CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    sku TEXT NOT NULL UNIQUE,
    price REAL NOT NULL,
    quantity INTEGER NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    phone TEXT,
    email TEXT,
    address TEXT,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS suppliers (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    phone TEXT,
    email TEXT,
    address TEXT,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS sales (
    id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    sale_date TEXT NOT NULL,
    total_amount REAL NOT NULL,
    created_at TEXT NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);

CREATE TABLE IF NOT EXISTS sale_items (
    id INTEGER PRIMARY KEY,
    sale_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price REAL NOT NULL,
    FOREIGN KEY (sale_id) REFERENCES sales(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);
"""


def get_schema_sql() -> str:
    return SCHEMA_SQL