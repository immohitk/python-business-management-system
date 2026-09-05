SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS schema_version (
    id INTEGER PRIMARY KEY,
    version TEXT NOT NULL
);

INSERT OR IGNORE INTO schema_version (id, version)
VALUES (1, '1');
"""


def get_schema_sql() -> str:
    return SCHEMA_SQL