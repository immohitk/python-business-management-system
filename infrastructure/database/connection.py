import sqlite3

from infrastructure.database import config


def get_connection() -> sqlite3.Connection:
    config.DATABASE_DIR.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(config.DATABASE_PATH)

    return connection