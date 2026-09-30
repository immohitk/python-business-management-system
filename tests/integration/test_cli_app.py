from pathlib import Path

from infrastructure.database.connection import get_connection
from infrastructure.database.initialization import initialize_database
from presentation.cli.app import run


def test_cli_app_runs_with_shared_context(
    tmp_path: Path,
    monkeypatch,
    capsys,
) -> None:
    database_path = tmp_path / "cli_app.db"

    initialize_database(database_path)

    monkeypatch.setattr(
        "presentation.cli.context.get_connection",
        lambda: get_connection(database_path),
    )

    inputs = iter(
        [
            "1",  # Products
            "0",  # Back to main menu
            "0",  # Exit application
        ]
    )

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs),
    )

    run()

    captured = capsys.readouterr()

    assert "Python Business Management System" in captured.out
    assert "Products" in captured.out
    assert "Exiting application..." in captured.out
