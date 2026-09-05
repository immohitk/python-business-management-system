from infrastructure.database.schema import get_schema_sql


def test_schema_sql_is_not_empty():
    assert get_schema_sql().strip()


def test_schema_sql_defines_schema_version_table():
    schema_sql = get_schema_sql()

    assert "CREATE TABLE IF NOT EXISTS schema_version" in schema_sql


def test_schema_sql_defines_version_column():
    schema_sql = get_schema_sql()

    assert "version TEXT NOT NULL" in schema_sql