from infrastructure.database.connection import get_connection
from infrastructure.database.schema import get_schema_sql


def initialize_database() -> None:
    connection = get_connection()

    try:
        connection.executescript(get_schema_sql())
        connection.commit()
    finally:
        connection.close()