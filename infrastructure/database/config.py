from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATABASE_DIR = PROJECT_ROOT / "data"

DATABASE_PATH = DATABASE_DIR / "business.db"