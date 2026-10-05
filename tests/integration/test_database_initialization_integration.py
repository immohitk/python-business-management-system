import sqlite3

from infrastructure.database.initialization import initialize_database


EXPECTED_TABLES = [
    "categories",
    "customers",
    "invoices",
    "product_history",
    "products",
    "sale_items",
    "sale_payments",
    "sale_tax_charge_snapshots",
    "sales",
    "schema_version",
    "stock_movements",
    "supplier_products",
    "suppliers",
    "taxes_charges",
    "units",
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

        assert result == (1, "4")
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
        assert schema_versions == [(1, "4")]
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



def _create_legacy_v1_database(database_path):
    connection = sqlite3.connect(database_path)
    try:
        connection.executescript(
            """
            CREATE TABLE schema_version (id INTEGER PRIMARY KEY, version TEXT NOT NULL);
            INSERT INTO schema_version VALUES (1, '1');
            CREATE TABLE products (id INTEGER PRIMARY KEY, name TEXT NOT NULL, description TEXT,
                sku TEXT NOT NULL UNIQUE, price REAL NOT NULL, quantity INTEGER NOT NULL, created_at TEXT NOT NULL);
            CREATE TABLE stock_movements (id INTEGER PRIMARY KEY, product_id INTEGER NOT NULL,
                movement_type TEXT NOT NULL, quantity INTEGER NOT NULL, resulting_stock INTEGER NOT NULL, created_at TEXT NOT NULL);
            CREATE TABLE product_history (id INTEGER PRIMARY KEY, product_id INTEGER, action TEXT NOT NULL,
                product_name TEXT NOT NULL, product_code TEXT NOT NULL, details TEXT, created_at TEXT NOT NULL);
            CREATE TABLE taxes_charges (id INTEGER PRIMARY KEY, name TEXT NOT NULL, type TEXT NOT NULL,
                calculation TEXT NOT NULL, value REAL NOT NULL, scope TEXT NOT NULL, product_id INTEGER,
                is_active INTEGER NOT NULL DEFAULT 1, created_at TEXT NOT NULL);
            CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT NOT NULL, phone TEXT, email TEXT,
                address TEXT, created_at TEXT NOT NULL);
            CREATE TABLE suppliers (id INTEGER PRIMARY KEY, name TEXT NOT NULL, phone TEXT, email TEXT,
                address TEXT, created_at TEXT NOT NULL);
            CREATE TABLE sales (id INTEGER PRIMARY KEY, customer_id INTEGER NOT NULL, sale_date TEXT NOT NULL,
                total_amount REAL NOT NULL, created_at TEXT NOT NULL);
            CREATE TABLE sale_items (id INTEGER PRIMARY KEY, sale_id INTEGER NOT NULL, product_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL, unit_price REAL NOT NULL);
            CREATE TABLE sale_payments (id INTEGER PRIMARY KEY, sale_id INTEGER NOT NULL, payment_mode TEXT NOT NULL,
                amount REAL NOT NULL, created_at TEXT NOT NULL);
            CREATE TABLE invoices (id INTEGER PRIMARY KEY, sale_id INTEGER NOT NULL, invoice_number TEXT NOT NULL UNIQUE,
                invoice_date TEXT NOT NULL, total_amount REAL NOT NULL, created_at TEXT NOT NULL);

            INSERT INTO products VALUES (1, 'Legacy Paint', 'Legacy product', 'LEG-001', 850.0, 25, '2026-01-01T10:00:00');
            INSERT INTO stock_movements VALUES (1, 1, 'PURCHASE', 25, 25, '2026-01-02T10:00:00');
            INSERT INTO product_history VALUES (1, 1, 'CREATED', 'Legacy Paint', 'LEG-001', 'legacy', '2026-01-01T10:00:00');
            INSERT INTO taxes_charges VALUES (1, 'Legacy GST', 'GST', 'PERCENTAGE', 18.0, 'GLOBAL', NULL, 1, '2026-01-01T10:00:00');
            INSERT INTO customers VALUES (1, 'Legacy Customer', '9000000001', 'legacy@example.com', 'Old Address', '2026-01-03T10:00:00');
            INSERT INTO suppliers VALUES (1, 'Legacy Supplier', '9000000002', 'supplier@example.com', 'Old Supplier Address', '2026-01-04T10:00:00');
            INSERT INTO sales VALUES (1, 1, '2026-01-05', 1700.0, '2026-01-05T10:00:00');
            INSERT INTO sale_items VALUES (1, 1, 1, 2, 850.0);
            INSERT INTO sale_payments VALUES (1, 1, 'CASH', 1700.0, '2026-01-05T10:00:00');
            INSERT INTO invoices VALUES (1, 1, 'INV-LEG-001', '2026-01-05', 1700.0, '2026-01-05T10:00:00');
            """
        )
        connection.commit()
    finally:
        connection.close()


def test_v2_migration_preserves_legacy_business_data(tmp_path):
    database_path = tmp_path / "legacy_v1.db"
    _create_legacy_v1_database(database_path)
    initialize_database(database_path)

    connection = sqlite3.connect(database_path)
    try:
        assert connection.execute("SELECT * FROM products WHERE id=1").fetchone()[:7] == (
            1, "Legacy Paint", "Legacy product", "LEG-001", 850.0, 25, "2026-01-01T10:00:00"
        )
        assert connection.execute("SELECT * FROM stock_movements WHERE id=1").fetchone() == (
            1, 1, "PURCHASE", 25, 25, "2026-01-02T10:00:00"
        )
        assert connection.execute("SELECT * FROM sales WHERE id=1").fetchone() == (
            1, 1, "2026-01-05", 1700.0, "2026-01-05T10:00:00"
        )
        assert connection.execute("SELECT * FROM sale_items WHERE id=1").fetchone() == (1, 1, 1, 2, 850.0)
        assert connection.execute("SELECT * FROM sale_payments WHERE id=1").fetchone() == (
            1, 1, "CASH", 1700.0, "2026-01-05T10:00:00"
        )
        assert connection.execute("SELECT * FROM invoices WHERE id=1").fetchone() == (
            1, 1, "INV-LEG-001", "2026-01-05", 1700.0, "2026-01-05T10:00:00"
        )
        assert connection.execute("SELECT base_unit, purchase_unit, sales_unit, quantity FROM products WHERE id=1").fetchone() == (
            "PCS", "PCS", "PCS", 25
        )
        assert connection.execute("SELECT city, state, pincode, status FROM customers WHERE id=1").fetchone() == (
            None, None, None, "ACTIVE"
        )
        assert connection.execute("SELECT tax_code, is_default FROM taxes_charges WHERE id=1").fetchone() == ("OTHER", 0)
        assert connection.execute("SELECT version FROM schema_version WHERE id=1").fetchone() == ("4",)
    finally:
        connection.close()


def test_v2_migration_is_idempotent_for_legacy_database(tmp_path):
    database_path = tmp_path / "legacy_v1.db"
    _create_legacy_v1_database(database_path)
    initialize_database(database_path)
    first = sqlite3.connect(database_path)
    try:
        first_product = first.execute("SELECT * FROM products WHERE id=1").fetchone()
        first_customer = first.execute("SELECT * FROM customers WHERE id=1").fetchone()
    finally:
        first.close()

    initialize_database(database_path)
    second = sqlite3.connect(database_path)
    try:
        assert second.execute("SELECT * FROM products WHERE id=1").fetchone() == first_product
        assert second.execute("SELECT * FROM customers WHERE id=1").fetchone() == first_customer
        assert second.execute("SELECT COUNT(*) FROM units").fetchone() == (9,)
    finally:
        second.close()
