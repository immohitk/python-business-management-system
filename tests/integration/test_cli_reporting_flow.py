from pathlib import Path

from infrastructure.database.connection import get_connection
from infrastructure.database.initialization import initialize_database
from presentation.cli.context import CLIContext
from presentation.cli.customers import add_customer
from presentation.cli.products import add_product
from presentation.cli.reports import handle_reports
from presentation.cli.sales import create_sale


def test_cli_reporting_uses_shared_application_context(
    tmp_path: Path,
    monkeypatch,
    capsys,
) -> None:
    database_path = tmp_path / "cli_reporting_flow.db"

    initialize_database(database_path)

    monkeypatch.setattr(
        "presentation.cli.context.get_connection",
        lambda: get_connection(database_path),
    )

    context = CLIContext()

    try:
        product_inputs = iter(
            [
                "Reporting Product",
                "Product used by reporting flow",
                "REPORT-001",
                "500",
                "10",
            ]
        )

        monkeypatch.setattr(
            "builtins.input",
            lambda _: next(product_inputs),
        )

        add_product(context.product_service)

        customer_inputs = iter(
            [
                "Reporting Customer",
                "9876543210",
                "report@example.com",
                "Bengaluru",
            ]
        )

        monkeypatch.setattr(
            "builtins.input",
            lambda _: next(customer_inputs),
        )

        add_customer(context.customer_service)

        sale_inputs = iter(
            [
                "1",
                "2026-09-30",
                "1",
                "2",
                "500",
                "n",
            ]
        )

        monkeypatch.setattr(
            "builtins.input",
            lambda _: next(sale_inputs),
        )

        create_sale(context.sale_service)

        capsys.readouterr()

        report_inputs = iter(
            [
                "2",
                "0",
            ]
        )

        monkeypatch.setattr(
            "builtins.input",
            lambda _: next(report_inputs),
        )

        handle_reports(context.reporting_service)

        captured = capsys.readouterr()

        assert "Sales Reports" in captured.out
        assert "Total sales: 1000.00" in captured.out
        assert "Reporting Product" in captured.out
        assert "Quantity: 2" in captured.out
        assert "Amount: 1000.00" in captured.out

        product = context.product_service.get_product(1)
        assert product is not None
        assert product.quantity == 8

    finally:
        context.close()
