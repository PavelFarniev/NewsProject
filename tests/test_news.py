"""Тесты класса News и функций для работы с новостями."""

import pytest

from models import Author, News
from models.news import (
    create_news,
    delete_news,
    filter_news_by_category,
    find_news,
    get_statistics,
    sort_news,
)

IVAN = Author(1, "Иван", "ivan@news.ru")
ANNA = Author(2, "Анна")


def make_news() -> list[News]:
    """Две новости для тестов."""
    news: list[News] = []
    create_news(news, "Новый смартфон", "Обзор", IVAN, "технологии",
                views=150, pub_date="2026-09-10")
    create_news(news, "Финал кубка", "Репортаж", ANNA, "Спорт",
                views=20, pub_date="2026-09-20")
    return news


def test_news_creation():
    item = News(1, "Заголовок", "Текст", IVAN, "спорт", 10, "2026-09-01")
    assert item.id == 1
    assert item.author is IVAN
    assert item.category == "Спорт"
    assert item.views == 10


def test_news_str():
    item = News(3, "Заголовок", "Текст", ANNA, "Погода")
    assert str(item) == "[3] Заголовок — Анна, Разное"


def test_views_only_through_method():
    item = News(1, "Т", "Т", IVAN, "Спорт", 99)
    assert item.register_view() == 100
    assert item.popularity() == "ПОПУЛЯРНАЯ"
    with pytest.raises(AttributeError):
        item.views = 0


def test_negative_views_forbidden():
    with pytest.raises(ValueError):
        News(1, "Т", "Т", IVAN, "Спорт", -1)


def test_create_news_returns_object():
    news: list[News] = []
    item = create_news(news, "Заголовок", "Текст", IVAN, "Спорт")
    assert isinstance(item, News)
    assert news == [item]


def test_create_news_without_author():
    with pytest.raises(ValueError):
        create_news([], "Заголовок", "Текст", None, "Спорт")


def test_create_news_empty_title():
    with pytest.raises(ValueError):
        create_news([], "", "Текст", IVAN, "Спорт")


def test_find_news():
    assert [item.id for item in find_news(make_news(), "СМАРТФОН")] == [1]


def test_filter_news_by_category():
    result = list(filter_news_by_category(make_news(), "спорт"))
    assert [item.id for item in result] == [2]


def test_sort_news_by_date():
    assert [item.id for item in sort_news(make_news(), key="date")] == [2, 1]


def test_delete_news():
    news = make_news()
    removed = delete_news(news, 1)
    assert removed is not None and removed.id == 1
    assert delete_news(news, 1) is None


def test_get_statistics():
    stats = get_statistics(make_news())
    assert stats["total"] == 2
    assert stats["total_views"] == 170
    assert stats["most_popular"].id == 1
