# APP Listing Publisher

Wersja: `0.1.5`

APP Listing Publisher to prototyp aplikacji do zarzadzania produktami przygotowywanymi do publikacji na portalach ogloszeniowych. Aktualna wersja obsluguje lokalny katalog produktow, zdjecia, migracje bazy danych oraz rejestrowanie publikacji ogloszen dla wybranych portali.

## Zakres Prototypu

Aktualnie aplikacja umozliwia:

- utworzenie lokalnej bazy danych,
- dodanie produktu do katalogu,
- wyswietlenie listy produktow,
- wyswietlenie szczegolow pojedynczego produktu,
- aktualizacje wybranych danych produktu,
- usuwanie produktu,
- obsluge zdjec produktow,
- migracje struktury bazy danych,
- utworzenie publikacji produktu dla wybranego portalu,
- wyswietlenie listy publikacji,
- wyswietlenie szczegolow pojedynczej publikacji,
- aktualizacje statusu publikacji,
- oznaczenie publikacji jako usunietej.

Produkt zawiera obecnie:

- tytul,
- opis,
- cene,
- kategorie,
- zdjecia.

## Plan Rozwoju

Najblizsze etapy rozwoju:

- tryb dry run dla publikacji,
- integracje z portalami ogloszeniowymi,
- automatyzacja przegladarki dla procesu publikacji,
- obsluge wyniku publikacji, w tym linku zewnetrznego i komunikatow bledow,
- walidacje statusow publikacji na poziomie modelu aplikacji.

## Architektura

Projekt jest podzielony na proste warstwy:

```text
APP_listing_pub/
├── listing_pub/
│   ├── __init__.py
│   ├── __main__.py
│   ├── cli.py
│   ├── config.py
│   ├── database.py
│   ├── models.py
│   └── services.py
├── migrations/
│   ├── 001_initial.sql
│   └── 002_create_listing_publications.sql
├── tests/
├── data/
├── photos/
├── requirements-dev.txt
├── README.md
└── .gitignore
```

Najwazniejsze moduly:

- `cli.py` - interfejs terminalowy i obsluga komend,
- `services.py` - logika aplikacji,
- `database.py` - operacje na bazie SQLite,
- `models.py` - modele danych,
- `config.py` - sciezki i konfiguracja lokalna,
- `__main__.py` - punkt startowy pakietu,
- `migrations/` - wersjonowane zmiany struktury bazy danych,
- `tests/` - testy automatyczne.

## Wymagania

- Python 3.11 lub nowszy
- SQLite dostepny w systemie

Do uruchamiania aplikacji nie sa wymagane zewnetrzne biblioteki.
Do uruchamiania testow wymagany jest `pytest` z `requirements-dev.txt`.

## Uruchomienie

Przejdz do katalogu projektu:

```bash
cd /Users/karoina/Documents/Codex/2026-06-15/APP_listing_pub
```

Wyswietl dostepne komendy:

```bash
python3 -m listing_pub --help
```

Utworz baze danych:

```bash
python3 -m listing_pub init-db
```

## Przyklady Uzycia

Dodanie produktu:

```bash
python3 -m listing_pub add-product \
  --title "Kurtka jeansowa" \
  --description "Stan bardzo dobry, rozmiar M" \
  --price 79.99 \
  --category "Ubrania" \
  --photo photos/photo.jpg
```

Lista produktow:

```bash
python3 -m listing_pub list-products
```

Szczegoly produktu:

```bash
python3 -m listing_pub show-product --id 1
```

Aktualizacja produktu:

```bash
python3 -m listing_pub update-product --id 1 --price 89.99 --category "Moda"
```

Dodanie publikacji produktu:

```bash
python3 -m listing_pub add-publication --product-id 1 --portal olx
```

Lista publikacji:

```bash
python3 -m listing_pub list-publications
```

Szczegoly publikacji:

```bash
python3 -m listing_pub show-publication --publication-id 1
```

Aktualizacja statusu publikacji:

```bash
python3 -m listing_pub update-publication-status --publication-id 1 --status publicated
```

Oznaczenie publikacji jako usunietej:

```bash
python3 -m listing_pub delete-publication --publication-id 1
```

Usuniecie produktu:

```bash
python3 -m listing_pub delete-product --id 1
```

## Testy

Testy automatyczne mozna uruchomic poleceniem:

```bash
python3 -m pytest
```

## Baza Danych

Aplikacja korzysta z lokalnej bazy SQLite:

```text
data/products.sqlite3
```

Aktualna tabela `products` przechowuje:

- `id`,
- `title`,
- `description`,
- `price`,
- `category`,
- `created_at`.

Tabela `product_photos` przechowuje:

- `id`,
- `product_id`,
- `path`,
- `position`.

Tabela `listing_publications` przechowuje:

- `id`,
- `product_id`,
- `portal`,
- `status`,
- `external_url`,
- `error_message`,
- `created_at`,
- `updated_at`.

Pomocne komendy diagnostyczne:

```bash
sqlite3 data/products.sqlite3 ".tables"
```

```bash
sqlite3 data/products.sqlite3 ".schema products"
```

```bash
sqlite3 data/products.sqlite3 "SELECT * FROM products;"
```

```bash
sqlite3 data/products.sqlite3 "SELECT * FROM product_photos;"
```

```bash
sqlite3 data/products.sqlite3 "SELECT * FROM listing_publications;"
```

## Status

Prototyp obsluguje podstawowy CRUD produktow, zapis sciezek zdjec, migracje bazy danych oraz zarzadzanie rekordami publikacji ogloszen w lokalnej bazie SQLite. Integracja z portalami ogloszeniowymi i automatyzacja przegladarki sa przewidziane w kolejnych etapach rozwoju.
