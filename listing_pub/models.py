from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path

ALLOWED_PHOTO_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
# TODO: zmiana na biblioteke pillow


@dataclass(frozen=True)
class Product:
    """Obiekt reprezentujacy jeden produkt w aplikacji.
    Obiekt Pythona, ktory wygodnie przenosi dane miedzy CLI a database.py.
    """

    id: int | None
    title: str
    description: str
    price: Decimal
    category: str
    photos: tuple[Path, ...]

    def validate(self) -> None:
        """Sprawdza podstawowe reguly przed zapisem produktu do bazy."""
        if not self.title.strip():
            raise ValueError("Tytul nie moze byc pusty.")
        if not self.description.strip():
            raise ValueError("Opis nie moze byc pusty.")
        if self.price <= 0:
            raise ValueError("Cena musi byc wieksza od 0.")
        if not self.category.strip():
            raise ValueError("Kategoria nie moze byc pusta.")
        if not self.photos:
            raise ValueError("Produkt musi miec przynajmniej jedno zdjecie.")

        for photo in self.photos:
            if photo.suffix.lower() not in ALLOWED_PHOTO_EXTENSIONS:
                raise ValueError(f"Nieobslugiwany format zdjecia: {photo}")


@dataclass(frozen=True)
class ListingPublication:
    """Obiekt reprezentujacy jedno ogloszenie w aplikacji."""

    id: int | None
    product_id: int
    portal: str
    status: str = "draft"
    external_url: str | None = None
    error_message: str | None = None