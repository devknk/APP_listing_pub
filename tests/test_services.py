from decimal import Decimal
from pathlib import Path

from listing_pub.database import add_db_product, get_db_publication, init_db
from listing_pub.models import Product
from listing_pub.services import (
    create_publication,
    delete_publication_by_id,
    update_publication_status,
)


def create_test_product(db_path: Path) -> int:
    product = Product(
        id=None,
        title="Testowy produkt",
        description="Opis testowego produktu",
        price=Decimal("10.90"),
        category="test",
        photos=(Path("photos/test.jpg"),),
    )

    return add_db_product(product, db_path=db_path)


def test_create_publication_for_existing_product(tmp_path) -> None:
    db_path = tmp_path / "products.sqlite3"
    init_db(db_path)

    product_id = create_test_product(db_path)

    publication = create_publication(product_id, portal="olx", db_path=db_path)

    assert publication.id == 1
    assert publication.product_id == product_id
    assert publication.portal == "olx"
    assert publication.status == "draft"
    assert publication.external_url is None
    assert publication.error_message is None


def test_update_existing_publication(tmp_path) -> None:
    db_path = tmp_path / "products.sqlite3"
    init_db(db_path)

    product_id = create_test_product(db_path)

    publication = create_publication(product_id, portal="vinted", db_path=db_path)

    updated_publication = update_publication_status(
        publication.id,
        status="deleted",
        db_path=db_path,
    )

    loaded_publication = get_db_publication(publication.id, db_path=db_path)

    assert updated_publication.status == "deleted"
    assert loaded_publication.status == "deleted"


def test_delete_publication_by_id(tmp_path) -> None:
    db_path = tmp_path / "products.sqlite3"
    init_db(db_path)

    product_id = create_test_product(db_path)
    publication = create_publication(product_id, portal="nieznany", db_path=db_path)
    deleted_publication = delete_publication_by_id(publication.id, db_path=db_path)
    loaded_publication = get_db_publication(publication.id, db_path=db_path)

    assert deleted_publication.id == loaded_publication.id
    assert loaded_publication.status == "deleted"
    assert loaded_publication.portal == "nieznany"
