from unittest.mock import Mock

from application.services.reporting_service import ReportingService


def test_get_business_summary_delegates_to_repository():
    repository = Mock()
    repository.get_business_summary.return_value = {
        "product_count": 2,
        "customer_count": 3,
        "supplier_count": 1,
        "sale_count": 4,
        "invoice_count": 4,
    }

    service = ReportingService(repository)

    result = service.get_business_summary()

    assert result == {
        "product_count": 2,
        "customer_count": 3,
        "supplier_count": 1,
        "sale_count": 4,
        "invoice_count": 4,
    }
    repository.get_business_summary.assert_called_once_with()


def test_get_sales_total_delegates_to_repository():
    repository = Mock()
    repository.get_sales_total.return_value = 1710.0

    service = ReportingService(repository)

    result = service.get_sales_total()

    assert result == 1710.0
    repository.get_sales_total.assert_called_once_with()


def test_get_sales_by_date_delegates_to_repository():
    repository = Mock()
    repository.get_sales_by_date.return_value = [
        {
            "sale_date": "2026-09-27",
            "sale_count": 2,
            "total_amount": 1470.0,
        }
    ]

    service = ReportingService(repository)

    result = service.get_sales_by_date()

    assert result == [
        {
            "sale_date": "2026-09-27",
            "sale_count": 2,
            "total_amount": 1470.0,
        }
    ]
    repository.get_sales_by_date.assert_called_once_with()


def test_get_sales_by_product_delegates_to_repository():
    repository = Mock()
    repository.get_sales_by_product.return_value = [
        {
            "product_id": 1,
            "product_name": "Paint",
            "quantity_sold": 3,
            "sales_amount": 1350.0,
        }
    ]

    service = ReportingService(repository)

    result = service.get_sales_by_product()

    assert result == [
        {
            "product_id": 1,
            "product_name": "Paint",
            "quantity_sold": 3,
            "sales_amount": 1350.0,
        }
    ]
    repository.get_sales_by_product.assert_called_once_with()


def test_get_stock_status_delegates_to_repository():
    repository = Mock()
    repository.get_stock_status.return_value = [
        {
            "product_id": 1,
            "product_name": "Paint",
            "sku": "PAINT-001",
            "quantity": 2,
        }
    ]

    service = ReportingService(repository)

    result = service.get_stock_status()

    assert result == [
        {
            "product_id": 1,
            "product_name": "Paint",
            "sku": "PAINT-001",
            "quantity": 2,
        }
    ]
    repository.get_stock_status.assert_called_once_with()


def test_get_stock_movements_summary_delegates_to_repository():
    repository = Mock()
    repository.get_stock_movements_summary.return_value = [
        {
            "movement_type": "ADD",
            "movement_count": 3,
            "total_quantity": 40,
        }
    ]

    service = ReportingService(repository)

    result = service.get_stock_movements_summary()

    assert result == [
        {
            "movement_type": "ADD",
            "movement_count": 3,
            "total_quantity": 40,
        }
    ]
    repository.get_stock_movements_summary.assert_called_once_with()


def test_get_low_stock_products_delegates_threshold_to_repository():
    repository = Mock()
    repository.get_low_stock_products.return_value = [
        {
            "product_id": 1,
            "product_name": "Paint",
            "sku": "PAINT-001",
            "quantity": 2,
        }
    ]

    service = ReportingService(repository)

    result = service.get_low_stock_products(5)

    assert result == [
        {
            "product_id": 1,
            "product_name": "Paint",
            "sku": "PAINT-001",
            "quantity": 2,
        }
    ]
    repository.get_low_stock_products.assert_called_once_with(5)


def test_get_customers_summary_delegates_to_repository():
    repository = Mock()
    repository.get_customers_summary.return_value = [
        {
            "customer_id": 1,
            "customer_name": "Customer A",
            "phone": "1111111111",
            "email": "a@example.com",
        }
    ]

    service = ReportingService(repository)

    result = service.get_customers_summary()

    assert result == repository.get_customers_summary.return_value
    repository.get_customers_summary.assert_called_once_with()


def test_get_suppliers_summary_delegates_to_repository():
    repository = Mock()
    repository.get_suppliers_summary.return_value = [
        {
            "supplier_id": 1,
            "supplier_name": "Supplier A",
            "phone": "3333333333",
            "email": "supplier-a@example.com",
        }
    ]

    service = ReportingService(repository)

    result = service.get_suppliers_summary()

    assert result == repository.get_suppliers_summary.return_value
    repository.get_suppliers_summary.assert_called_once_with()
