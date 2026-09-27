"""Тесты класса Comment и функций для комментариев."""

import pytest

from models import Author, Comment, News
from models.comments import (
    add_comment,
    delete_comment,
    delete_comments_for_news,
    get_comments_for_news,
)

AUTHOR = Author(1, "Иван")
NEWS_1 = News(1, "Первая", "Текст", AUTHOR, "Спорт")
NEWS_2 = News(2, "Вторая", "Текст", AUTHOR, "Культура")


def test_comment_links_to_news():
    comment = Comment(1, NEWS_1, "Максим", "Отлично")
    assert comment.news is NEWS_1
    assert comment.news.author.name == "Иван"


def test_comment_str():
    assert str(Comment(1, NEWS_1, "Максим", "Привет")) == "Максим: Привет"
    assert str(Comment(2, NEWS_1, "", "Привет")) == "Аноним: Привет"


def test_add_comment():
    comments: list[Comment] = []
    add_comment(comments, NEWS_1, "Максим", "Отлично")
    add_comment(comments, NEWS_2, "", "Норм")
    assert [c.text for c in get_comments_for_news(comments, NEWS_1)] == [
        "Отлично"
    ]


def test_add_comment_to_missing_news():
    with pytest.raises(LookupError):
        add_comment([], None, "Максим", "Текст")


def test_add_empty_comment():
    with pytest.raises(ValueError):
        add_comment([], NEWS_1, "Максим", "   ")


def test_delete_comment():
    comments: list[Comment] = []
    add_comment(comments, NEWS_1, "", "Текст")
    assert delete_comment(comments, 1)
    assert not delete_comment(comments, 1)


def test_delete_comments_for_news():
    comments: list[Comment] = []
    add_comment(comments, NEWS_1, "", "a")
    add_comment(comments, NEWS_1, "", "b")
    add_comment(comments, NEWS_2, "", "c")
    assert delete_comments_for_news(comments, NEWS_1) == 2
    assert [c.news for c in comments] == [NEWS_2]
