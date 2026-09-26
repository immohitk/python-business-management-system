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


def test_handle_choice_products(capsys, monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "0")

    result = handle_choice("1")

    captured = capsys.readouterr()

    assert result is True
    assert "Products" in captured.out


def test_handle_choice_inventory(capsys, monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "0")

    result = handle_choice("2")

    captured = capsys.readouterr()

    assert result is True
    assert "Inventory" in captured.out


def test_handle_choice_sales(capsys, monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "0")

    result = handle_choice("3")

    captured = capsys.readouterr()

    assert result is True
    assert "Sales" in captured.out
    assert "1. Create sale" in captured.out
    assert "2. List sales" in captured.out
    assert "0. Back" in captured.out


def test_handle_choice_customers(capsys, monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "0")

    result = handle_choice("4")

    captured = capsys.readouterr()

    assert result is True
    assert "Customers" in captured.out


def test_handle_choice_suppliers(capsys, monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "0")

    result = handle_choice("5")

    captured = capsys.readouterr()

    assert result is True
    assert "Suppliers" in captured.out


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


def test_handle_products(capsys, monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "0")

    handle_products()

    captured = capsys.readouterr()

    assert "Products" in captured.out


def test_handle_inventory(capsys):
    handle_inventory()

    captured = capsys.readouterr()

    assert "Inventory menu" in captured.out


def test_handle_sales(capsys, monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "0")

    handle_sales()

    captured = capsys.readouterr()

    assert "Sales" in captured.out
    assert "1. Create sale" in captured.out
    assert "2. List sales" in captured.out
    assert "0. Back" in captured.out


def test_handle_customers(capsys, monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "0")

    handle_customers()

    captured = capsys.readouterr()

    assert "Customers" in captured.out


def test_handle_suppliers(capsys, monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "0")

    handle_suppliers()

    captured = capsys.readouterr()

    assert "Suppliers" in captured.out


def test_handle_inventory(capsys, monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "0")

    handle_inventory()

    captured = capsys.readouterr()

    assert "Inventory" in captured.out
    assert "1. View stock" in captured.out
    assert "2. Stock in" in captured.out
    assert "3. Adjust stock" in captured.out
    assert "4. Stock out" in captured.out
    assert "5. View movement history" in captured.out
    assert "0. Back" in captured.out


def test_handle_choice_invoices(capsys, monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "0")

    result = handle_choice("6")

    captured = capsys.readouterr()

    assert result is True
    assert "Invoices" in captured.out
    assert "1. Show invoice" in captured.out
    assert "0. Back" in captured.out
