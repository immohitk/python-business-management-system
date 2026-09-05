from presentation.cli.app import run


def test_cli_runs(capsys):
    run()

    captured = capsys.readouterr()

    assert "Python Business Management System" in captured.out
    assert "Application starting..." in captured.out
