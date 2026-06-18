from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class Product:
    """Obiekt reprezentujacy jeden produkt w aplikacji.Obiekt Pythona,
    ktory wygodnie przenosi dane miedzy CLI a database.py.
    """

    id: int | None
    title: str
    description: str
    price: Decimal
    category: str

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
