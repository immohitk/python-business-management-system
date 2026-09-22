from unittest.mock import Mock, patch

from presentation.cli.sales import create_sale_service, handle_sales


def test_create_sale_service_builds_sale_service():
    service, connection = create_sale_service()

    try:
        assert service.sale_repository is not None
        assert service.inventory_service is not None
        assert service.sale_repository.connection is connection
    finally:
        connection.close()


@patch("presentation.cli.sales.create_sale_service")
def test_handle_sales_back(mock_create_service):
    service = Mock()
    connection = Mock()
    mock_create_service.return_value = service, connection

    with patch("builtins.input", return_value="0"):
        handle_sales()

    mock_create_service.assert_called_once()
    connection.close.assert_called_once()


def test_handle_sales_accepts_injected_service():
    service = Mock()

    with patch("builtins.input", side_effect=["0"]):
        handle_sales(service)
