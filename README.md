# APP Listing Publisher

Wersja: `0.1.3`

APP Listing Publisher to pierwszy prototyp aplikacji do zarzadzania produktami przygotowywanymi do publikacji na portalach ogloszeniowych. Aktualna wersja koncentruje sie na podstawowym katalogu produktow oraz lokalnej bazie SQLite, ktora stanowi fundament pod kolejne etapy: obsluge zdjec, statusow publikacji i integracji z portalami.

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
- zapis informacji o publikacjach ogloszen na portalach,
- utworzenie publikacji produktu przez CLI.

Produkt zawiera obecnie:

- tytul,
- opis,
- cene,
- kategorie,
- zdjecia.

## Plan Rozwoju

Najblizsze etapy rozwoju:

- obsluge zmian statusow publikacji,
- kolejne komendy CLI do zarzadzania publikacjami,
- tryb dry run dla publikacji,
- integracje z portalami ogloszeniowymi,
- automatyzacja przegladarki dla procesu publikacji.

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
├── data/
├── photos/
├── learnings/
├── README.md
└── .gitignore
```

Najwazniejsze moduly:

- `cli.py` - interfejs terminalowy i obsluga komend,
- `services.py` - logika aplikacji,
- `database.py` - operacje na bazie SQLite,
- `models.py` - modele danych,
- `config.py` - sciezki i konfiguracja lokalna,
- `__main__.py` - punkt startowy pakietu.

## Wymagania

- Python 3.11 lub nowszy
- SQLite dostepny w systemie

Projekt nie wymaga obecnie zewnetrznych bibliotek.
Do uruchamiania testow developerskich wymagany jest pytest z requirements-dev.txt.

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

Prototyp obsluguje podstawowy CRUD produktow, zapis sciezek zdjec oraz podstawowy zapis publikacji ogloszen w lokalnej bazie SQLite.
