from infrastructure.database.connection import get_connection


def initialize_database() -> None:
    connection = get_connection()

    try:
        connection.commit()
    finally:
        connection.close()