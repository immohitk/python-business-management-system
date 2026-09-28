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

    def get_customers_summary(self) -> list[dict[str, object]]:
        rows = self.connection.execute(
            """
            SELECT
                id,
                name,
                phone,
                email
            FROM customers
            ORDER BY id
            """
        ).fetchall()

        return [
            {
                "customer_id": row[0],
                "customer_name": row[1],
                "phone": row[2],
                "email": row[3],
            }
            for row in rows
        ]

    def get_suppliers_summary(self) -> list[dict[str, object]]:
        rows = self.connection.execute(
            """
            SELECT
                id,
                name,
                phone,
                email
            FROM suppliers
            ORDER BY id
            """
        ).fetchall()

        return [
            {
                "supplier_id": row[0],
                "supplier_name": row[1],
                "phone": row[2],
                "email": row[3],
            }
            for row in rows
        ]

    def get_sales_total(self) -> float:
        row = self.connection.execute(
            """
            SELECT COALESCE(SUM(total_amount), 0)
            FROM sales
            """
        ).fetchone()

        return float(row[0])

    def get_sales_by_date(self) -> list[dict[str, object]]:
        rows = self.connection.execute(
            """
            SELECT
                sale_date,
                COUNT(*) AS sale_count,
                COALESCE(SUM(total_amount), 0) AS total_amount
            FROM sales
            GROUP BY sale_date
            ORDER BY sale_date
            """
        ).fetchall()

        return [
            {
                "sale_date": row[0],
                "sale_count": row[1],
                "total_amount": float(row[2]),
            }
            for row in rows
        ]

    def get_sales_by_product(self) -> list[dict[str, object]]:
        rows = self.connection.execute(
            """
            SELECT
                sale_items.product_id,
                products.name,
                SUM(sale_items.quantity) AS quantity_sold,
                SUM(sale_items.quantity * sale_items.unit_price) AS sales_amount
            FROM sale_items
            JOIN products
                ON products.id = sale_items.product_id
            GROUP BY sale_items.product_id, products.name
            ORDER BY sale_items.product_id
            """
        ).fetchall()

        return [
            {
                "product_id": row[0],
                "product_name": row[1],
                "quantity_sold": row[2],
                "sales_amount": float(row[3]),
            }
            for row in rows
        ]


    def get_stock_status(self) -> list[dict[str, object]]:
        rows = self.connection.execute(
            """
            SELECT
                id,
                name,
                sku,
                quantity
            FROM products
            ORDER BY id
            """
        ).fetchall()

        return [
            {
                "product_id": row[0],
                "product_name": row[1],
                "sku": row[2],
                "quantity": row[3],
            }
            for row in rows
        ]

    def get_stock_movements_summary(self) -> list[dict[str, object]]:
        rows = self.connection.execute(
            """
            SELECT
                movement_type,
                COUNT(*) AS movement_count,
                COALESCE(SUM(quantity), 0) AS total_quantity
            FROM stock_movements
            GROUP BY movement_type
            ORDER BY movement_type
            """
        ).fetchall()

        return [
            {
                "movement_type": row[0],
                "movement_count": row[1],
                "total_quantity": row[2],
            }
            for row in rows
        ]

    def get_low_stock_products(
        self,
        threshold: int,
    ) -> list[dict[str, object]]:
        rows = self.connection.execute(
            """
            SELECT
                id,
                name,
                sku,
                quantity
            FROM products
            WHERE quantity <= ?
            ORDER BY quantity, id
            """,
            (threshold,),
        ).fetchall()

        return [
            {
                "product_id": row[0],
                "product_name": row[1],
                "sku": row[2],
                "quantity": row[3],
            }
            for row in rows
        ]
