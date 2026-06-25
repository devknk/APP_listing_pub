from pathlib import Path


# BASE_DIR wskazuje glowny folder projektu.
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
PHOTOS_DIR = BASE_DIR / "photos"
DB_PATH = DATA_DIR / "products.sqlite3"
MIGRATIONS_DIR = BASE_DIR / "migrations"
