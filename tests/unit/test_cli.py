from presentation.cli.app import handle_choice, run

from presentation.cli.products import handle_products


def test_handle_choice_exit(capsys):
    result = handle_choice("0")

    captured = capsys.readouterr()

    assert result is False
    assert "Exiting application..." in captured.out


def test_handle_choice_products(capsys):
    result = handle_choice("1")

    captured = capsys.readouterr()

    assert result is True
    assert "Products menu" in captured.out


def test_handle_choice_invalid_option(capsys):
    result = handle_choice("9")

    captured = capsys.readouterr()

    assert result is True
    assert "Invalid choice" in captured.out


def test_run_exits(capsys, monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "0")

    run()

    captured = capsys.readouterr()

    assert "Python Business Management System" in captured.out
    assert "Exiting application..." in captured.out


def test_handle_products(capsys):
    handle_products()

    captured = capsys.readouterr()

    assert "Products menu" in captured.out
