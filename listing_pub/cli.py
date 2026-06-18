import argparse
from decimal import Decimal, InvalidOperation

from .database import init_db
from .services import (
    create_product,
    get_product_by_id,
    get_products,
    update_product_details,
    delete_product_by_id,
)


def parse_price(value: str) -> Decimal:
    """Zamienia tekst z terminala na Decimal.

    Decimal jest lepszy do cen niz float, bo unika typowych bledow zaokraglen.
    """
    try:
        price = Decimal(value.replace(",", "."))
    except InvalidOperation as exc:
        raise argparse.ArgumentTypeError("Cena musi byc liczba, np. 79.99.") from exc

    if price <= 0:
        raise argparse.ArgumentTypeError("Cena musi byc wieksza od 0.")
    return price


def build_parser() -> argparse.ArgumentParser:
    """Definiuje komendy dostepne w terminalu."""
    parser = argparse.ArgumentParser( # tworzy parser
        prog="listing-pub",
        description="Baza produktow w SQLite.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True) # beda rozne komendy

    subparsers.add_parser("init-db", help="Tworzy baze danych.") # dodaje komende

    add_parser = subparsers.add_parser("add-product", help="Dodaje produkt.")
    add_parser.add_argument("--title", required=True)
    add_parser.add_argument("--description", required=True)
    add_parser.add_argument("--price", required=True, type=parse_price)
    add_parser.add_argument("--category", required=True)

    subparsers.add_parser("list-products", help="Pokazuje liste produktow.")

    show_parser = subparsers.add_parser("show-product", help="Pokazuje jeden produkt.")
    show_parser.add_argument("--id", required=True, type=int)

    update_parser = subparsers.add_parser("update-product", help="Aktualizuje produkt.")
    update_parser.add_argument("--id", required=True, type=int)
    update_parser.add_argument("--title")
    update_parser.add_argument("--description")
    update_parser.add_argument("--price", type=parse_price)
    update_parser.add_argument("--category")

    delete_parser = subparsers.add_parser("delete-product", help="Usun produkt.")
    delete_parser.add_argument("--id", required=True, type=int)

    return parser


def handle_init_db() -> None:
    init_db()
    print("Baza danych gotowa.")


def handle_add_product(args: argparse.Namespace) -> None:
    product_id = create_product(
        title=args.title,
        description=args.description,
        price=args.price,
        category=args.category,
    )
    print(f"Dodano produkt id={product_id}.")


def handle_list_products() -> None:
    products = get_products()

    if not products:
        print("Brak produktow w bazie.")
        return

    for product in products:
        print(f"[{product.id}] {product.title} | {product.price} PLN | {product.category}")


def handle_show_product(args: argparse.Namespace) -> None:
    product = get_product_by_id(args.id)

    print(f"ID: {product.id}")
    print(f"Tytul: {product.title}")
    print(f"Opis: {product.description}")
    print(f"Cena: {product.price} PLN")
    print(f"Kategoria: {product.category}")


def handle_update_product(args: argparse.Namespace) -> None:
    try:
        product = update_product_details(
            product_id=args.id,
            title=args.title,
            description=args.description,
            price=args.price,
            category=args.category,
        )
    except (LookupError, ValueError) as exc:
        print(f"Blad: {exc}")
        return

    print(f"Zaktualizowano produkt id={product.id}.")
    print(f"Tytul: {product.title}")
    print(f"Opis: {product.description}")
    print(f"Cena: {product.price} PLN")
    print(f"Kategoria: {product.category}")


def handle_delete_product(args: argparse.Namespace) -> None:
    try:
        deleted_product = delete_product_by_id(args.id)
    except LookupError as exc:
        print(f"Blad: {exc}")
        return

    print(f"Usunieto produkt {deleted_product.title} o id={deleted_product.id}.")


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "init-db":
        handle_init_db()
    elif args.command == "add-product":
        handle_add_product(args)
    elif args.command == "list-products":
        handle_list_products()
    elif args.command == "show-product":
        handle_show_product(args)
    elif args.command == "update-product":
        handle_update_product(args)
    elif args.command == "delete-product":
        handle_delete_product(args)
    else:
        parser.error("Nieznana komenda.")
