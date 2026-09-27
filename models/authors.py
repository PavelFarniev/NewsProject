"""Класс Author и функции для работы со списком авторов."""


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
