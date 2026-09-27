"""Тесты функций работы с новостями."""

import pytest

from news import (
    assign_category,
    create_news,
    delete_news,
    filter_news_by_category,
    find_news,
    get_statistics,
    rate_popularity,
    register_view,
    sort_news,
)


def make_news() -> list[dict]:
    """Подготовить список из двух новостей для тестов."""
    news: list[dict] = []
    create_news(news, "Новый смартфон", "Обзор", "Иван", "технологии",
                views=150, pub_date="2026-09-10")
    create_news(news, "Финал кубка", "Репортаж", "Анна", "Спорт",
                views=20, pub_date="2026-09-20")
    return news


def test_create_news():
    news: list[dict] = []
    item = create_news(news, "Заголовок", "Текст", "Автор", "Спорт")
    assert len(news) == 1
    assert item["id"] == 1
    assert item["category"] == "Спорт"


def test_create_news_empty_title_raises():
    with pytest.raises(ValueError):
        create_news([], "", "Текст", "Автор", "Спорт")


def test_assign_category_unknown():
    assert assign_category("Погода") == "Разное"
    assert assign_category("") == "Разное"


def test_rate_popularity():
    assert rate_popularity(1000).startswith("ВИРУСНАЯ")
    assert rate_popularity(150) == "ПОПУЛЯРНАЯ"


def test_find_news_case_insensitive():
    news = make_news()
    assert [item["id"] for item in find_news(news, "СМАРТФОН")] == [1]


def test_filter_news_by_category():
    news = make_news()
    result = list(filter_news_by_category(news, "спорт"))
    assert [item["id"] for item in result] == [2]


def test_sort_news_by_date():
    news = make_news()
    assert [item["id"] for item in sort_news(news, key="date")] == [2, 1]


def test_register_view_missing_news():
    with pytest.raises(KeyError):
        register_view(make_news(), 99)


def test_delete_news_removes_comments():
    news = make_news()
    comments = [{"id": 1, "news_id": 1, "author": "", "text": "ok"}]
    assert delete_news(news, comments, 1)
    assert len(news) == 1
    assert comments == []


def test_get_statistics():
    stats = get_statistics(make_news())
    assert stats["total"] == 2
    assert stats["total_views"] == 170
    assert stats["most_popular"]["id"] == 1
