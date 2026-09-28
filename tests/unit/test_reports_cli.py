from presentation.cli.reports import (
    handle_reports,
    show_business_summary,
    show_sales_reports,
    show_inventory_reports,
    show_customer_reports,
    show_supplier_reports,
)


class FakeReportingService:
    def get_business_summary(self):
        return {
            "product_count": 2,
            "customer_count": 1,
            "supplier_count": 1,
            "sale_count": 3,
            "invoice_count": 2,
        }

    def get_sales_total(self):
        return 1710.0

    def get_sales_by_date(self):
        return [
            {
                "sale_date": "2026-09-27",
                "sale_count": 2,
                "total_amount": 1470.0,
            }
        ]

    def get_sales_by_product(self):
        return [
            {
                "product_id": 1,
                "product_name": "Paint",
                "quantity_sold": 3,
                "sales_amount": 1350.0,
            }
        ]

    def get_stock_status(self):
        return [
            {
                "product_id": 1,
                "product_name": "Paint",
                "sku": "PAINT-001",
                "quantity": 2,
            }
        ]

    def get_stock_movements_summary(self):
        return [
            {
                "movement_type": "ADD",
                "movement_count": 3,
                "total_quantity": 40,
            }
        ]

    def get_low_stock_products(self, threshold):
        return [
            {
                "product_id": 1,
                "product_name": "Paint",
                "sku": "PAINT-001",
                "quantity": 2,
            }
        ]

    def get_customers_summary(self):
        return [
            {
                "customer_id": 1,
                "customer_name": "Alice",
                "phone": "1234567890",
                "email": "alice@example.com",
            }
        ]

    def get_suppliers_summary(self):
        return [
            {
                "supplier_id": 1,
                "supplier_name": "Supplier A",
                "phone": "9876543210",
                "email": "supplier@example.com",
            }
        ]


def test_handle_reports_exit(capsys, monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "0")

    handle_reports(FakeReportingService())

    captured = capsys.readouterr()

    assert "Reports" in captured.out
    assert "1. Business summary" in captured.out
    assert "2. Sales reports" in captured.out
    assert "3. Inventory reports" in captured.out
    assert "4. Customer reports" in captured.out
    assert "5. Supplier reports" in captured.out


def test_show_business_summary(capsys):
    show_business_summary(FakeReportingService())

    captured = capsys.readouterr()

    assert "Business Summary" in captured.out
    assert "product_count: 2" in captured.out
    assert "sale_count: 3" in captured.out


def test_show_sales_reports(capsys):
    show_sales_reports(FakeReportingService())

    captured = capsys.readouterr()

    assert "Sales Reports" in captured.out
    assert "Total sales: 1710.00" in captured.out
    assert "2026-09-27" in captured.out
    assert "Paint" in captured.out


def test_show_inventory_reports(capsys, monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "5")

    show_inventory_reports(FakeReportingService())

    captured = capsys.readouterr()

    assert "Inventory Reports" in captured.out
    assert "Stock Status" in captured.out
    assert "Stock Movement Summary" in captured.out
    assert "Low Stock Products" in captured.out
    assert "Paint" in captured.out


def test_show_customer_reports(capsys):
    show_customer_reports(FakeReportingService())

    captured = capsys.readouterr()

    assert "Customer Reports" in captured.out
    assert "Alice" in captured.out


def test_show_supplier_reports(capsys):
    show_supplier_reports(FakeReportingService())

    captured = capsys.readouterr()

    assert "Supplier Reports" in captured.out
    assert "Supplier A" in captured.out
