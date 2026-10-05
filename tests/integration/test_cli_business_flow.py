from pathlib import Path

from infrastructure.database.connection import get_connection
from infrastructure.database.initialization import initialize_database
from presentation.cli.context import CLIContext
from presentation.cli.customers import add_customer
from presentation.cli.invoices import create_invoice_from_sale, show_invoice
from presentation.cli.products import add_product
from presentation.cli.sales import create_sale


def test_cli_business_flow_product_customer_sale_invoice(
    tmp_path: Path,
    monkeypatch,
    capsys,
) -> None:
    database_path = tmp_path / "cli_business_flow.db"

    initialize_database(database_path)

    monkeypatch.setattr(
        "presentation.cli.context.get_connection",
        lambda: get_connection(database_path),
    )

    context = CLIContext()

    try:
        product_inputs = iter(
            [
                "CLI Business Product",
                "Product used by integrated CLI flow",
                "CLI-FLOW-001",
                "1000",
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
                "CLI Business Customer",
                "9876543210",
                "cli@example.com",
                "Bengaluru",
                "Bengaluru",
                "Karnataka",
                "560001",
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
                "1000",
                "n",
            ]
        )

        monkeypatch.setattr(
            "builtins.input",
            lambda _: next(sale_inputs),
        )

        create_sale(context.sale_service)

        captured = capsys.readouterr()

        assert "Product added successfully with ID: 1" in captured.out
        assert "Customer added successfully with ID: 1" in captured.out
        assert "Sale created successfully with ID: 1" in captured.out
        assert "total: 2000.00" in captured.out

        invoice_inputs = iter(["1"])

        monkeypatch.setattr(
            "builtins.input",
            lambda _: next(invoice_inputs),
        )

        create_invoice_from_sale(context.sale_invoice_service)

        captured = capsys.readouterr()

        assert "Invoice created successfully: INV-000001" in captured.out

        invoice_show_inputs = iter(["1"])

        monkeypatch.setattr(
            "builtins.input",
            lambda _: next(invoice_show_inputs),
        )

        show_invoice(context.invoice_presentation_service)

        captured = capsys.readouterr()

        assert "TAX INVOICE" in captured.out
        assert "INV-000001" in captured.out
        assert "CLI Business Customer" in captured.out
        assert "CLI Business Product" in captured.out
        assert "CLI-FLOW-001" in captured.out
        assert "2000.00" in captured.out

        product = context.product_service.get_product(1)
        assert product is not None
        assert product.quantity == 8

        sale = context.sale_service.get_sales()[0]
        assert sale.total_amount == 2000.0

    finally:
        context.close()
