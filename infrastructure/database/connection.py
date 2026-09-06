import sqlite3
from pathlib import Path

from infrastructure.database import config


def get_connection(database_path: Path | None = None) -> sqlite3.Connection:
    path = database_path or config.DATABASE_PATH

    path.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(path)

    return connection