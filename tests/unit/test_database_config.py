from pathlib import Path

from infrastructure.database.config import DATABASE_DIR, DATABASE_PATH, PROJECT_ROOT


def test_project_root_exists():
    assert PROJECT_ROOT.exists()
    assert PROJECT_ROOT.is_dir()


def test_database_directory_is_inside_project_root():
    assert DATABASE_DIR.parent == PROJECT_ROOT


def test_database_path_points_to_database_file():
    assert DATABASE_PATH.parent == DATABASE_DIR
    assert DATABASE_PATH.name == "business.db"