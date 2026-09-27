"""Тесты функций работы с комментариями."""

import pytest

from comments import (
    add_comment,
    delete_comment,
    format_comment,
    get_comments_for_news,
)

NEWS = [{"id": 1, "title": "T", "text": "X", "author": "A",
         "category": "Спорт", "views": 0, "pub_date": "2026-09-01"}]


def test_add_comment():
    comments: list[dict] = []
    add_comment(comments, NEWS, 1, "Максим", "Отлично")
    assert get_comments_for_news(comments, 1)[0]["text"] == "Отлично"


def test_add_comment_to_missing_news():
    with pytest.raises(KeyError):
        add_comment([], NEWS, 5, "Максим", "Текст")


def test_add_empty_comment():
    with pytest.raises(ValueError):
        add_comment([], NEWS, 1, "Максим", "   ")


def test_delete_comment():
    comments: list[dict] = []
    add_comment(comments, NEWS, 1, "", "Текст")
    assert delete_comment(comments, 1)
    assert not delete_comment(comments, 1)


def test_format_comment_anonymous():
    assert format_comment("Привет", "") == "Аноним: Привет"
