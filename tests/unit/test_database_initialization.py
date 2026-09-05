from infrastructure.database.initialization import initialize_database


def test_initialize_database_completes_successfully():
    initialize_database()


def test_initialize_database_creates_database_file():
    from infrastructure.database.config import DATABASE_PATH

    initialize_database()

    assert DATABASE_PATH.exists()
    assert DATABASE_PATH.is_file()