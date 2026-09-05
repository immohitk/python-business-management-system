import sqlite3

from infrastructure.database.config import DATABASE_DIR, DATABASE_PATH


def get_connection() -> sqlite3.Connection:
    DATABASE_DIR.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DATABASE_PATH)

    return connection