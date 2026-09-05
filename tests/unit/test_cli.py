from presentation.cli.app import handle_choice, run

from presentation.cli.products import handle_products

from presentation.cli.inventory import handle_inventory

from presentation.cli.sales import handle_sales

from presentation.cli.customers import handle_customers

from presentation.cli.suppliers import handle_suppliers

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


def test_handle_choice_inventory(capsys):
    result = handle_choice("2")

    captured = capsys.readouterr()

    assert result is True
    assert "Inventory menu" in captured.out


def test_handle_choice_sales(capsys):
    result = handle_choice("3")

    captured = capsys.readouterr()

    assert result is True
    assert "Sales menu" in captured.out


def test_handle_choice_customers(capsys):
    result = handle_choice("4")

    captured = capsys.readouterr()

    assert result is True
    assert "Customers menu" in captured.out


def test_handle_choice_suppliers(capsys):
    result = handle_choice("5")

    captured = capsys.readouterr()

    assert result is True
    assert "Suppliers menu" in captured.out


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


def test_handle_inventory(capsys):
    handle_inventory()

    captured = capsys.readouterr()

    assert "Inventory menu" in captured.out


def test_handle_sales(capsys):
    handle_sales()

    captured = capsys.readouterr()

    assert "Sales menu" in captured.out


def test_handle_customers(capsys):
    handle_customers()

    captured = capsys.readouterr()

    assert "Customers menu" in captured.out


def test_handle_suppliers(capsys):
    handle_suppliers()

    captured = capsys.readouterr()

    assert "Suppliers menu" in captured.out
