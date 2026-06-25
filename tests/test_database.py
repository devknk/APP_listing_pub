from decimal import Decimal
from pathlib import Path

from listing_pub.database import add_product, get_product, init_db, run_migrations
from listing_pub.models import Product


def test_add_product_saves_photos(tmp_path):
    db_path = tmp_path / "products.sqlite3"  # wskazanie sciezki tmp

    init_db(db_path)  # zainicjowanie bazy w tmp_path

    photo_1 = Path("photos/test1.jpg")  # testowe sciezki do zdjec
    photo_2 = Path("photos/test2.jpg")

    product = Product(  # utworz testowy produkt
        id=None,
        title="Testowy tytul",
        description="Testowy opis",
        category="testowa",
        price=Decimal("12.00"),
        photos=(photo_1, photo_2),
    )

    product_id = add_product(product, db_path=db_path)  # dodaj produkt do bazy i zwroc id
    loaded_product = get_product(product_id, db_path=db_path)

    assert loaded_product.id == product_id
    assert loaded_product.photos == (photo_1, photo_2)


def test_run_migrations(tmp_path):
    db_path = tmp_path / "products.sqlite3"

    first_run = run_migrations(db_path=db_path)
    second_run = run_migrations(db_path=db_path)
    assert first_run == ["001_initial.sql"]
    assert second_run == []