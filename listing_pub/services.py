from decimal import Decimal
from pathlib import Path

from .config import DB_PATH
from .database import (
    add_db_publication,
    add_db_product,
    delete_db_product,
    get_db_publication,
    get_db_product,
    init_db,
    list_publications,
    list_products,
    update_db_publication,
    update_db_product,
)
from .models import ListingPublication, Product, PublicationDryRun


def create_publication(
    product_id: int,
    portal: str,
    db_path: Path = DB_PATH,
) -> ListingPublication:
    init_db(db_path)
    get_db_product(product_id, db_path=db_path)

    publication = ListingPublication(
        id=None,
        product_id=product_id,
        portal=portal,
        status="draft",
    )

    publication_id = add_db_publication(publication, db_path=db_path)

    return get_db_publication(publication_id, db_path=db_path)


def create_product(
    title: str,
    description: str,
    price: Decimal,
    category: str,
    photos: tuple[Path, ...],
) -> int:
    init_db()
    product = Product(
        id=None,
        title=title,
        description=description,
        price=price,
        category=category,
        photos=photos,
    )
    return add_db_product(product)


def get_publications() -> list[ListingPublication]:
    init_db()
    return list_publications()


def get_publication_by_id(publication_id: int) -> ListingPublication:
    init_db()

    return get_db_publication(publication_id)


def get_products() -> list[Product]:
    init_db()
    return list_products()


def get_product_by_id(product_id: int) -> Product:
    init_db()
    return get_db_product(product_id)


def prepare_publication_dry_run(
    publication_id: int,
    db_path: Path = DB_PATH,
) -> PublicationDryRun:
    init_db(db_path)
    publication = get_db_publication(publication_id, db_path=db_path)
    product = get_db_product(publication.product_id, db_path=db_path)
    if not product.photos:
        raise ValueError("Nie mozna opublikowac produktu bez zdjec.")

    publication_dry_run = PublicationDryRun(
        publication_id=publication_id,
        portal=publication.portal,
        product_title=product.title,
        price=product.price,
        photo_count=len(product.photos),
        steps=(
            f"Otworz portal {publication.portal}",
            "Zaloguj uzytkownika",
            "Przejdz do formularza dodawania ogloszenia",
            "Wpisz tytul produktu",
            "Wpisz opis produktu",
            "Ustaw cene",
            "Wybierz kategorie",
            "Dodaj zdjecia",
            "Kliknij publikuj",
        ),
    )
    return publication_dry_run


def update_publication_status(
    publication_id: int,
    status: str,
    db_path: Path = DB_PATH,
) -> ListingPublication:
    init_db(db_path)

    if status is None:
        raise ValueError("Podaj status do aktualizacji")

    current_publication = get_db_publication(publication_id, db_path=db_path)
    updated_publication = ListingPublication(
        id=current_publication.id,
        product_id=current_publication.product_id,
        portal=current_publication.portal,
        status=status,
        external_url=current_publication.external_url,
        error_message=current_publication.error_message,
    )
    update_db_publication(updated_publication, db_path=db_path)
    return updated_publication


def update_product_details(
    product_id: int,
    title: str | None = None,
    description: str | None = None,
    price: Decimal | None = None,
    category: str | None = None,
    photos: tuple[Path, ...] | None = None,
) -> Product:
    init_db()

    if (
        title is None
        and description is None
        and price is None
        and category is None
        and photos is None
    ):
        raise ValueError("Podaj przynajmniej jedno pole do aktualizacji.")

    current_product = get_db_product(product_id)
    updated_product = Product(
        id=current_product.id,
        title=title if title is not None else current_product.title,
        description=description if description is not None else current_product.description,
        price=price if price is not None else current_product.price,
        category=category if category is not None else current_product.category,
        photos=photos if photos is not None else current_product.photos,
    )
    update_db_product(updated_product)
    return updated_product


def delete_publication_by_id(publication_id: int, db_path: Path = DB_PATH) -> ListingPublication:
    """Oznacza publikacje jako usunieta."""
    init_db(db_path)
    loaded_publication = get_db_publication(publication_id, db_path=db_path)
    updated_publication = update_publication_status(
        loaded_publication.id,
        status="deleted",
        db_path=db_path,
    )
    # TODO: mechanizm usuniecia ogloszenia na portalu
    return updated_publication


def delete_product_by_id(product_id: int) -> Product:
    init_db()
    deleted_product = get_db_product(product_id)
    delete_db_product(product_id)
    return deleted_product
