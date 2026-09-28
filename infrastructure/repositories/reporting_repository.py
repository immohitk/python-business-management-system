from sqlite3 import Connection


class ReportingRepository:
    """SQLite repository for read-only reporting queries."""

    def __init__(self, connection: Connection) -> None:
        self.connection = connection

    def get_business_summary(self) -> dict[str, int]:
        product_count = self.connection.execute(
            "SELECT COUNT(*) FROM products"
        ).fetchone()[0]

        customer_count = self.connection.execute(
            "SELECT COUNT(*) FROM customers"
        ).fetchone()[0]

        supplier_count = self.connection.execute(
            "SELECT COUNT(*) FROM suppliers"
        ).fetchone()[0]

        sale_count = self.connection.execute(
            "SELECT COUNT(*) FROM sales"
        ).fetchone()[0]

        invoice_count = self.connection.execute(
            "SELECT COUNT(*) FROM invoices"
        ).fetchone()[0]

        return {
            "product_count": product_count,
            "customer_count": customer_count,
            "supplier_count": supplier_count,
            "sale_count": sale_count,
            "invoice_count": invoice_count,
        }
