import sqlite3
from decimal import Decimal
from pathlib import Path

from .config import DATA_DIR, DB_PATH, PHOTOS_DIR
from .models import Product


# SQL tworzacy pierwsza tabele w projekcie.
SCHEMA = """
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    price TEXT NOT NULL,
    category TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
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

    # row_factory sprawia, ze wynik SELECT mozna czytac po nazwie kolumny,
    # np. row["title"], zamiast po indeksie, np. row[1].
    connection.row_factory = sqlite3.Row
    return connection


def init_db(db_path: Path = DB_PATH) -> None:
    """Tworzy tabele potrzebne aplikacji."""
    with connect(db_path) as connection:
        connection.executescript(SCHEMA)


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
        return int(cursor.lastrowid)


def list_products(db_path: Path = DB_PATH) -> list[Product]:
    """Pobiera wszystkie produkty z bazy."""
    with connect(db_path) as connection:
        rows = connection.execute(
            "SELECT * FROM products ORDER BY created_at DESC, id DESC"
        ).fetchall()

    return [
        Product(
            id=int(row["id"]),
            title=row["title"],
            description=row["description"],
            price=Decimal(row["price"]),
            category=row["category"],
        )
        for row in rows
    ]


def get_product(product_id: int, db_path: Path = DB_PATH) -> Product:
    """Pobiera jeden produkt po id."""
    with connect(db_path) as connection:
        row = connection.execute(
            "SELECT * FROM products WHERE id = ?",
            (product_id,),
        ).fetchone()

    if row is None:
        raise LookupError(f"Nie znaleziono produktu o id={product_id}.")

    return Product(
        id=int(row["id"]),
        title=row["title"],
        description=row["description"],
        price=Decimal(row["price"]),
        category=row["category"],
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
