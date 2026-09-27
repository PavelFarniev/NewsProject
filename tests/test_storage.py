"""Тесты загрузки и сохранения объектов в JSON."""

import json

from models import Author, Comment, News
from storage import (
    load_authors,
    load_comments,
    load_list,
    load_news,
    save_authors,
    save_comments,
    save_news,
)


def test_load_missing_file(tmp_path):
    assert load_list(tmp_path / "missing.json") == []


def test_load_broken_json(tmp_path):
    filename = tmp_path / "broken.json"
    filename.write_text("{не json", encoding="utf-8")
    assert load_list(filename) == []


def test_save_and_load_objects(tmp_path):
    ivan = Author(1, "Иван", "ivan@news.ru")
    item = News(1, "Заголовок", "Текст", ivan, "Спорт", 5, "2026-09-01")
    comment = Comment(1, item, "Максим", "Круто")
    save_authors([ivan], tmp_path / "a.json")
    save_news([item], tmp_path / "n.json")
    save_comments([comment], tmp_path / "c.json")

    authors = load_authors(tmp_path / "a.json")
    news = load_news(authors, tmp_path / "n.json")
    comments = load_comments(news, tmp_path / "c.json")

    assert news[0].author is authors[0]
    assert comments[0].news is news[0]
    assert news[0].views == 5
    assert str(comments[0]) == "Максим: Круто"


def test_news_saved_with_author_id(tmp_path):
    item = News(1, "Т", "Т", Author(7, "Анна"), "Спорт")
    save_news([item], tmp_path / "n.json")
    data = json.loads((tmp_path / "n.json").read_text(encoding="utf-8"))
    assert data[0]["author_id"] == 7
    assert "author" not in data[0]


def test_news_with_unknown_author_skipped(tmp_path):
    filename = tmp_path / "n.json"
    filename.write_text(json.dumps([{
        "id": 1, "title": "Т", "text": "Т", "author_id": 99,
        "category": "Спорт", "views": 0, "pub_date": "2026-09-01",
    }]), encoding="utf-8")
    assert load_news([Author(1, "Иван")], filename) == []
