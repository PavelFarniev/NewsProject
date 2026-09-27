"""Класс Comment и функции для работы с комментариями."""

from .news import News


class Comment:
    """Комментарий читателя к конкретной новости."""

    def __init__(
        self, comment_id: int, news: News, author_name: str, text: str
    ) -> None:
        """Создать комментарий. Новость хранится как объект News."""
        self.id = comment_id
        self.news = news
        self.author_name = author_name
        self.text = text

    def __str__(self) -> str:
        """Комментарий в виде «Имя: текст» (add_comment из ПР1)."""
        if not self.text:
            return "Комментариев пока нет."
        if not self.author_name:
            return f"Аноним: {self.text}"
        return f"{self.author_name}: {self.text}"
