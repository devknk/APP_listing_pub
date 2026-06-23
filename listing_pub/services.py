from decimal import Decimal
from pathlib import Path

from .database import (
    add_product,
    delete_product,
    get_product,
    init_db,
    list_products,
    update_product,
)

from .models import Product


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
    return add_product(product)


def get_products() -> list[Product]:
    init_db()
    return list_products()


def get_product_by_id(product_id: int) -> Product:
    init_db()
    return get_product(product_id)


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

    current_product = get_product(product_id)
    updated_product = Product(
        id=current_product.id,
        title=title if title is not None else current_product.title,
        description=description if description is not None else current_product.description,
        price=price if price is not None else current_product.price,
        category=category if category is not None else current_product.category,
        photos=photos if photos is not None else current_product.photos,
    )
    update_product(updated_product)
    return updated_product


def delete_product_by_id(product_id: int) -> Product:
    init_db()
    deleted_product = get_product(product_id)
    delete_product(product_id)
    return deleted_product
