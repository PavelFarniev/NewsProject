"""Класс Comment и функции для работы с комментариями."""

from utils import next_id

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


def add_comment(
    comments: list[Comment],
    news_item: News | None,
    author_name: str,
    text: str,
) -> Comment:
    """Создать комментарий к новости, добавить в список и вернуть.

    LookupError — если новости нет, ValueError — если текст пустой.
    """
    if news_item is None:
        raise LookupError("Новость не найдена.")
    if not text.strip():
        raise ValueError("Ошибка: текст комментария не может быть пустым.")
    comment = Comment(
        next_id(comments), news_item, author_name.strip(), text.strip()
    )
    comments.append(comment)
    return comment


def get_comments_for_news(
    comments: list[Comment], news_item: News
) -> list[Comment]:
    """Все комментарии к конкретной новости."""
    return [comment for comment in comments if comment.news is news_item]


def delete_comment(comments: list[Comment], comment_id: int) -> bool:
    """Удалить комментарий по id; True, если он был."""
    for comment in comments:
        if comment.id == comment_id:
            comments.remove(comment)
            return True
    return False


def delete_comments_for_news(
    comments: list[Comment], news_item: News
) -> int:
    """Удалить все комментарии к новости и вернуть, сколько удалено."""
    before = len(comments)
    comments[:] = [c for c in comments if c.news is not news_item]
    return before - len(comments)
