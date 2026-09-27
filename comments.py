"""Функции работы с комментариями к новостям."""

from news import get_news_by_id
from utils import next_id


def format_comment(comment_text: str, commenter_name: str) -> str:
    """Вернуть строку комментария для вывода (функция add_comment из ПР1)."""
    if len(comment_text) == 0:
        return "Комментариев пока нет."
    if len(commenter_name) == 0:
        return f"Аноним: {comment_text}"
    return f"{commenter_name}: {comment_text}"


def add_comment(
    comments: list[dict],
    news: list[dict],
    news_id: int,
    author: str,
    text: str,
) -> dict:
    """Добавить комментарий к новости и вернуть его словарь.

    KeyError — если новости нет, ValueError — если текст пустой.
    """
    if get_news_by_id(news, news_id) is None:
        raise KeyError(news_id)
    if not text.strip():
        raise ValueError("Ошибка: текст комментария не может быть пустым.")
    comment = {
        "id": next_id(comments),
        "news_id": news_id,
        "author": author.strip(),
        "text": text.strip(),
    }
    comments.append(comment)
    return comment


def get_comments_for_news(comments: list[dict], news_id: int) -> list[dict]:
    """Вернуть список комментариев к новости с идентификатором news_id."""
    return [comment for comment in comments if comment["news_id"] == news_id]


def delete_comment(comments: list[dict], comment_id: int) -> bool:
    """Удалить комментарий по идентификатору; True, если он был удален."""
    for index, comment in enumerate(comments):
        if comment["id"] == comment_id:
            del comments[index]
            return True
    return False
