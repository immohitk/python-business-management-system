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
