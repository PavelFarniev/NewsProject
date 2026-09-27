"""Класс Author и функции для работы со списком авторов."""

from utils import next_id


class Author:
    """Автор, который публикует новости."""

    def __init__(self, author_id: int, name: str, email: str = "") -> None:
        """Создать автора с идентификатором, именем и почтой."""
        self.id = author_id
        self.name = name
        self.email = email

    @classmethod
    def from_data(cls, data: dict) -> "Author":
        """Создать автора из словаря, прочитанного из JSON."""
        return cls(data["id"], data["name"], data.get("email", ""))

    @staticmethod
    def is_valid_email(email: str) -> bool:
        """Проверить почту: пустая строка или адрес вида name@site.ru."""
        if email == "":
            return True
        name, _, domain = email.partition("@")
        return bool(name) and "." in domain

    def __str__(self) -> str:
        """Имя автора и почта в скобках, если она указана."""
        if self.email:
            return f"{self.name} ({self.email})"
        return self.name


def add_author(authors: list[Author], name: str, email: str = "") -> Author:
    """Создать автора, добавить его в список и вернуть.

    Если имя пустое или почта неправильная, выбрасывается ValueError.
    """
    name = name.strip()
    email = email.strip()
    if not name:
        raise ValueError("Ошибка: имя автора не может быть пустым.")
    if not Author.is_valid_email(email):
        raise ValueError("Ошибка: неправильный адрес почты.")
    author = Author(next_id(authors), name, email)
    authors.append(author)
    return author


def get_author_by_id(authors: list[Author], author_id: int) -> Author | None:
    """Найти автора по id; если его нет, вернуть None."""
    return next((a for a in authors if a.id == author_id), None)


def find_author(authors: list[Author], query: str) -> list[Author]:
    """Найти авторов по части имени или почты (без учета регистра)."""
    needle = query.strip().lower()
    return [
        author for author in authors
        if needle in author.name.lower() or needle in author.email.lower()
    ]
