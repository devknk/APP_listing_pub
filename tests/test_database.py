from decimal import Decimal
from pathlib import Path

from listing_pub.database import (
    add_listing_publication,
    add_product,
    get_listing_publication,
    get_product,
    init_db,
    run_migrations,
)
from listing_pub.models import ListingPublication, Product


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
    assert first_run == [
        "001_initial.sql",
        "002_create_listing_publications.sql",
    ]
    assert second_run == []


def test_add_listing_publication(tmp_path):
    db_path = tmp_path / "products.sqlite3"
    init_db(db_path)

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

    product_id = add_product(product, db_path=db_path)

    listing = ListingPublication(
        id=None,
        product_id=product_id,
        portal="olx",
        status="draft",
        external_url="www.olx.pl",
        error_message=None,
    )

    listing_id = add_listing_publication(listing, db_path=db_path)
    assert listing_id == 1

    loaded_listing = get_listing_publication(listing_id, db_path=db_path)

    assert loaded_listing.id == listing_id
    assert loaded_listing.product_id == product_id
    assert loaded_listing.portal == "olx"
    assert loaded_listing.status == "draft"
    assert loaded_listing.external_url == "www.olx.pl"
    assert loaded_listing.error_message is None