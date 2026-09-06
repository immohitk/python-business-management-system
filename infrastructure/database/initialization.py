from pathlib import Path

from infrastructure.database.connection import get_connection
from infrastructure.database.schema import get_schema_sql


def initialize_database(database_path: Path | None = None) -> None:
    connection = get_connection(database_path)

    try:
        connection.executescript(get_schema_sql())
        connection.commit()
    finally:
        connection.close()