"""Тесты класса Author и функций для авторов."""

import pytest

from models import Author
from models.authors import add_author, find_author, get_author_by_id


def test_author_creation():
    author = Author(1, "Иван Петров", "ivan@news.ru")
    assert author.id == 1
    assert author.name == "Иван Петров"
    assert author.email == "ivan@news.ru"


def test_author_str():
    assert str(Author(1, "Иван", "ivan@news.ru")) == "Иван (ivan@news.ru)"
    assert str(Author(2, "Анна")) == "Анна"


def test_author_from_data():
    author = Author.from_data({"id": 5, "name": "Ольга", "email": ""})
    assert isinstance(author, Author)
    assert author.id == 5
    assert author.name == "Ольга"


def test_is_valid_email():
    assert Author.is_valid_email("")
    assert Author.is_valid_email("a@b.ru")
    assert not Author.is_valid_email("просто текст")


def test_add_and_find_author():
    authors: list[Author] = []
    add_author(authors, "Иван Петров", "ivan@news.ru")
    anna = add_author(authors, "Анна Смирнова")
    assert anna.id == 2
    assert get_author_by_id(authors, 2) is anna
    assert find_author(authors, "ИВАН")[0].name == "Иван Петров"


def test_add_author_bad_email():
    with pytest.raises(ValueError):
        add_author([], "Иван", "ivan-news.ru")
