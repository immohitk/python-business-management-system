from contextlib import contextmanager
from contextvars import ContextVar
import sqlite3


_transaction_connections: ContextVar[set[int]] = ContextVar(
    "transaction_connections",
    default=set(),
)


@contextmanager
def transaction(connection: sqlite3.Connection):
    connections = _transaction_connections.get()
    updated_connections = connections | {id(connection)}
    token = _transaction_connections.set(updated_connections)

    connection.execute("BEGIN")

    try:
        yield connection
    except Exception:
        connection.rollback()
        raise
    else:
        connection.commit()
    finally:
        _transaction_connections.reset(token)


def is_transaction_active(connection: sqlite3.Connection) -> bool:
    return id(connection) in _transaction_connections.get()


def commit_if_needed(connection: sqlite3.Connection) -> None:
    if not is_transaction_active(connection):
        connection.commit()
