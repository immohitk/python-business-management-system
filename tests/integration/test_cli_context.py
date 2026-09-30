from pathlib import Path

from infrastructure.database.connection import get_connection
from infrastructure.database.initialization import initialize_database
from presentation.cli.context import CLIContext


def test_cli_context_shares_one_database_connection(
    tmp_path: Path,
    monkeypatch,
) -> None:
    database_path = tmp_path / "cli_context.db"

    initialize_database(database_path)
    monkeypatch.setattr(
        "presentation.cli.context.get_connection",
        lambda: get_connection(database_path),
    )

    context = CLIContext()

    try:
        assert context.product_service.repository.connection is context.connection
        assert (
            context.inventory_service.product_repository.connection
            is context.connection
        )
        assert (
            context.sale_service.sale_repository.connection
            is context.connection
        )
        assert (
            context.invoice_presentation_service.invoice_repository.connection
            is context.connection
        )
        assert context.reporting_service.repository.connection is context.connection
    finally:
        context.close()
