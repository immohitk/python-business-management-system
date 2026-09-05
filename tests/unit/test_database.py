import sqlite3

from infrastructure.database.initialization import initialize_database


def test_database_initialization_creates_expected_schema(tmp_path, monkeypatch):
    database_path = tmp_path / "test_business.db"

    monkeypatch.setattr(
        "infrastructure.database.config.DATABASE_DIR",
        database_path.parent,
    )
    monkeypatch.setattr(
        "infrastructure.database.config.DATABASE_PATH",
        database_path,
    )

    initialize_database()

    assert database_path.exists()

    connection = sqlite3.connect(database_path)

    try:
        table = connection.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table' AND name = 'schema_version'
            """
        ).fetchone()

        version = connection.execute(
            "SELECT id, version FROM schema_version"
        ).fetchone()

        assert table == ("schema_version",)
        assert version == (1, "1")
    finally:
        connection.close()