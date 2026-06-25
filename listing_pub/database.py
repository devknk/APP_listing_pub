import sqlite3
from decimal import Decimal
from pathlib import Path

from .config import DATA_DIR, DB_PATH, MIGRATIONS_DIR, PHOTOS_DIR
from .models import Product


MIGRATIONS_TABLE = """
CREATE TABLE IF NOT EXISTS schema_migrations (
    version TEXT PRIMARY KEY,
    applied_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
"""


def connect(db_path: Path = DB_PATH) -> sqlite3.Connection:
    """Otwiera polaczenie z baza SQLite.

    SQLite przechowuje baze w zwyklym pliku. Jesli plik jeszcze nie istnieje,
    zostanie utworzony przy pierwszym polaczeniu.
    """
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    PHOTOS_DIR.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(db_path)

    # row_factory pozwala czytac wynik SELECT po nazwie kolumny,
    # np. row["title"], zamiast po indeksie, np. row[1].
    connection.row_factory = sqlite3.Row
    return connection


def init_db(db_path: Path = DB_PATH) -> None:
    """Tworzy lub aktualizuje strukture bazy danych."""
    run_migrations(db_path)


def migration_files(migrations_dir: Path = MIGRATIONS_DIR) -> list[Path]:
    if not migrations_dir.exists():
        return []
    return sorted(migrations_dir.glob("*.sql"))


def applied_migrations(connection: sqlite3.Connection) -> set[str]:
    connection.execute(MIGRATIONS_TABLE)
    rows = connection.execute("SELECT version FROM schema_migrations").fetchall()
    return {row["version"] for row in rows}


def run_migrations(db_path: Path = DB_PATH) -> list[str]:
    applied_now: list[str] = []

    with connect(db_path) as connection:
        applied = applied_migrations(connection)
        for migration_file in migration_files():
            version = migration_file.name
            if version in applied:
                continue
            sql = migration_file.read_text(encoding="utf-8")
            connection.executescript(sql)
            connection.execute(
                "INSERT INTO schema_migrations (version) VALUES (?)",
                (version,),
            )
            applied_now.append(version)

    return applied_now


def add_product(product: Product, db_path: Path = DB_PATH) -> int:
    """Dodaje produkt do bazy i zwraca jego nowe id."""
    product.validate()

    with connect(db_path) as connection:
        cursor = connection.execute(
            """
            INSERT INTO products (title, description, price, category)
            VALUES (?, ?, ?, ?)
            """,
            (
                product.title.strip(),
                product.description.strip(),
                str(product.price),
                product.category.strip(),
            ),
        )
        product_id = int(cursor.lastrowid)
        connection.executemany(
            """
            INSERT INTO product_photos (product_id, path, position)
            VALUES (?, ?, ?)
            """,
            [
                (product_id, str(photo), index)
                for index, photo in enumerate(product.photos)
            ],
        )
        return product_id


def list_products(db_path: Path = DB_PATH) -> list[Product]:
    """Pobiera wszystkie produkty z bazy."""
    with connect(db_path) as connection:
        rows = connection.execute(
            "SELECT * FROM products ORDER BY created_at DESC, id DESC"
        ).fetchall()
        products: list[Product] = []
        for row in rows:
            photo_rows = connection.execute(
                """
                SELECT path FROM product_photos
                WHERE product_id = ?
                ORDER BY position, id
                """,
                (row["id"],),
            ).fetchall()

            product = Product(
                id=int(row["id"]),
                title=row["title"],
                description=row["description"],
                price=Decimal(row["price"]),
                category=row["category"],
                photos=tuple(Path(photo_row["path"]) for photo_row in photo_rows),
            )

            products.append(product)

    return products


def get_product(product_id: int, db_path: Path = DB_PATH) -> Product:
    """Pobiera jeden produkt po id."""
    with connect(db_path) as connection:
        row = connection.execute(
            "SELECT * FROM products WHERE id = ?",
            (product_id,),
        ).fetchone()

        if row is None:
            raise LookupError(f"Nie znaleziono produktu o id={product_id}.")

        photo_rows = connection.execute(
            """
            SELECT path FROM product_photos
            WHERE product_id = ?
            ORDER BY position, id
            """,
            (product_id,),
        ).fetchall()

    return Product(
        id=int(row["id"]),
        title=row["title"],
        description=row["description"],
        price=Decimal(row["price"]),
        category=row["category"],
        photos=tuple(Path(photo_row["path"]) for photo_row in photo_rows),
    )


def update_product(product: Product, db_path: Path = DB_PATH) -> None:
    """Aktualizuje istniejacy produkt w bazie."""
    if product.id is None:
        raise ValueError("Nie mozna aktualizowac produktu bez id.")

    product.validate()

    with connect(db_path) as connection:
        cursor = connection.execute(
            """
            UPDATE products
            SET title = ?, description = ?, price = ?, category = ?
            WHERE id = ?
            """,
            (
                product.title.strip(),
                product.description.strip(),
                str(product.price),
                product.category.strip(),
                product.id,
            ),
        )

    if cursor.rowcount == 0:
        raise LookupError(f"Nie znaleziono produktu o id={product.id}.")


def delete_product(product_id: int, db_path: Path = DB_PATH) -> None:
    """Usuwa produkt z bazy po id."""
    with connect(db_path) as connection:
        cursor = connection.execute(
            "DELETE FROM products WHERE id = ?",
            (product_id,),
        )
    if cursor.rowcount == 0:
        raise LookupError(f"Nie znaleziono produktu o id={product_id}.")
