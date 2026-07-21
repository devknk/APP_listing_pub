import argparse
from decimal import Decimal, InvalidOperation
from pathlib import Path

from .database import init_db
from .services import (
    create_publication,
    create_product,
    delete_publication_by_id,
    delete_product_by_id,
    get_publications,
    get_publication_by_id,
    get_product_by_id,
    get_products,
    update_publication_status,
    update_product_details,
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


def parse_photo_path(value: str) -> Path:
    path = Path(value)

    if not path.exists():
        raise argparse.ArgumentTypeError(f"Plik nie istnieje: {path}")

    if not path.is_file():
        raise argparse.ArgumentTypeError(f"Sciezka nie jest plikiem: {path}")

    return path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(  # tworzy parser
        prog="listing-pub",
        description="Baza produktow w SQLite.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)  # beda rozne komendy

    subparsers.add_parser("init-db", help="Tworzy baze danych.")  # dodaje komende

    add_parser = subparsers.add_parser("add-product", help="Dodaje produkt.")
    add_parser.add_argument("--title", required=True)
    add_parser.add_argument("--description", required=True)
    add_parser.add_argument("--price", required=True, type=parse_price)
    add_parser.add_argument("--category", required=True)
    add_parser.add_argument(
        "--photo",
        action="append",
        required=True,
        type=parse_photo_path,
    )

    subparsers.add_parser("list-products", help="Pokazuje liste produktow.")
    subparsers.add_parser("list-publications", help="Pokazuje liste ogloszen.")

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

    add_pub_parser = subparsers.add_parser("add-publication", help="Dodaje publikacje produktu.")
    add_pub_parser.add_argument("--product-id", required=True, type=int)
    add_pub_parser.add_argument("--portal", required=True, help="Nazwa portalu, np. olx.")

    show_pub_parser = subparsers.add_parser("show-publication", help="Pokazuje ogloszenie.")
    show_pub_parser.add_argument("--publication-id", required=True, type=int)

    delete_pub_parser = subparsers.add_parser("delete-publication", help="Usun ogloszenie.")
    delete_pub_parser.add_argument("--publication-id", required=True, type=int)

    update_pub_parser = subparsers.add_parser("update-publication-status", help="Aktualizuje status ogloszenia.")
    update_pub_parser.add_argument("--publication-id", required=True, type=int)
    update_pub_parser.add_argument("--status", required=True, choices=["draft", "published", "deleted"])

    return parser


def handle_init_db() -> None:
    init_db()
    print("Baza danych gotowa.")


def handle_add_publication(args: argparse.Namespace) -> None:
    publication = create_publication(
        product_id=args.product_id,
        portal=args.portal,
    )
    print(
        f"Dodano publikacje id={publication.id} "
        f"dla produktu id={publication.product_id} "
        f"na portalu {publication.portal} ze statusem {publication.status}."
    )


def handle_add_product(args: argparse.Namespace) -> None:
    product_id = create_product(
        title=args.title,
        description=args.description,
        price=args.price,
        category=args.category,
        photos=tuple(args.photo),
    )
    print(f"Dodano produkt id={product_id}.")


def handle_list_publications(args: argparse.Namespace) -> None:
    publications = get_publications()

    if not publications:
        print("Nie ma ogloszen w bazie")
        return

    for publication in publications:
        print(
            f"[{publication.id}] "
            f"{publication.portal} "
            f"{publication.status} "
        )


def handle_list_products(args: argparse.Namespace) -> None:
    products = get_products()

    if not products:
        print("Brak produktow w bazie.")
        return

    for product in products:
        print(
            f"[{product.id}] {product.title} "
            f"| {product.price} PLN | {product.category} "
            f"| {product.description} | zdjecia: {len(product.photos)}"
        )


def handle_show_publication(args: argparse.Namespace) -> None:
    publication = get_publication_by_id(args.publication_id)

    print(f"[{publication.id}] ")
    print(f"{publication.portal} | {publication.status} ")


def handle_show_product(args: argparse.Namespace) -> None:
    product = get_product_by_id(args.id)

    print(f"ID: {product.id}")
    print(f"Tytul: {product.title}")
    print(f"Opis: {product.description}")
    print(f"Cena: {product.price} PLN")
    print(f"Kategoria: {product.category}")
    print("Zdjecia:")
    for photo in product.photos:
        print(f"- {photo}")


def handle_update_publication_status(args: argparse.Namespace) -> None:
    try:
        publication = update_publication_status(args.publication_id, args.status)
    except (LookupError, ValueError) as exc:
        print(f"Blad: {exc}")
        return
    print(f"Zaktualizowano status ogloszenia o id: {publication.id}")
    print(f"Aktualny status: {publication.status}")

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


def handle_delete_publication(args: argparse.Namespace) -> None:
    try:
        deleted_publication = delete_publication_by_id(args.publication_id)
    except LookupError as exc:
        print(f"Blad: {exc}")
        return

    print(f"Usunieto z portalu {deleted_publication.portal} ogloszenie id={deleted_publication.id}.")


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
    elif args.command == "add-publication":
        handle_add_publication(args)
    elif args.command == "add-product":
        handle_add_product(args)
    elif args.command == "list-publications":
        handle_list_publications(args)
    elif args.command == "list-products":
        handle_list_products(args)
    elif args.command == "show-publication":
        handle_show_publication(args)
    elif args.command == "show-product":
        handle_show_product(args)
    elif args.command == "update-publication-status":
        handle_update_publication_status(args)
    elif args.command == "update-product":
        handle_update_product(args)
    elif args.command == "delete-publication":
        handle_delete_publication(args)
    elif args.command == "delete-product":
        handle_delete_product(args)
    else:
        parser.error("Nieznana komenda.")
