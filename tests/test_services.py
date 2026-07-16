from decimal import Decimal
from pathlib import Path

from listing_pub.database import add_product, init_db
from listing_pub.models import Product
from listing_pub.services import create_listing_publication


def test_create_listing_publication_for_existing_product(tmp_path) -> None:
    db_path = tmp_path / "products.sqlite3"
    init_db(db_path)

    product = Product(
        id=None,
        title="Testowy produkt",
        description="Opis produktu",
        price=Decimal("10.00"),
        category="test",
        photos=(Path("photos/test.jpg"),),
    )

    product_id = add_product(product, db_path=db_path)

    publication = create_listing_publication(product_id, portal="olx", db_path=db_path)

    assert publication.id == 1
    assert publication.product_id == product_id
    assert publication.portal == "olx"
    assert publication.status == "draft"
    assert publication.external_url is None
    assert publication.error_message is None
