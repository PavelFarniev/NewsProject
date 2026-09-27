"""Загрузка и сохранение данных в JSON.

В файлах лежат обычные словари, а программа работает с объектами.
Здесь происходит перевод в обе стороны: JSON -> объекты при загрузке
и объекты -> JSON при сохранении. Связи (автор новости, новость
комментария) в JSON хранятся как id и восстанавливаются при загрузке.
"""

import json
from pathlib import Path

from models import Author, Comment, News
from models.authors import get_author_by_id
from models.news import get_news_by_id

DATA_DIR = Path(__file__).parent / "data"
AUTHORS_FILE = DATA_DIR / "authors.json"
NEWS_FILE = DATA_DIR / "news.json"
COMMENTS_FILE = DATA_DIR / "comments.json"


def load_list(filename: Path) -> list[dict]:
    """Прочитать список словарей из JSON-файла.

    Если файла нет или он испорчен, возвращается пустой список
    и печатается сообщение.
    """
    try:
        with open(filename, encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"Файл {filename.name} не найден, начинаем с пустых данных.")
        return []
    except json.JSONDecodeError:
        print(f"Файл {filename.name} поврежден (некорректный JSON).")
        return []
    if not isinstance(data, list):
        print(f"Файл {filename.name} должен содержать список записей.")
        return []
    return data


def save_list(filename: Path, items: list[dict]) -> bool:
    """Записать список словарей в JSON-файл. True, если все получилось."""
    try:
        filename.parent.mkdir(parents=True, exist_ok=True)
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(items, file, ensure_ascii=False, indent=4)
    except OSError as error:
        print(f"Не удалось сохранить {filename.name}: {error}")
        return False
    return True


def load_authors(filename: Path = AUTHORS_FILE) -> list[Author]:
    """Загрузить авторов и вернуть список объектов Author."""
    authors = []
    for data in load_list(filename):
        try:
            authors.append(Author.from_data(data))
        except (KeyError, TypeError):
            print(f"Пропущена битая запись автора: {data}")
    return authors


def save_authors(authors: list[Author], filename: Path = AUTHORS_FILE) -> bool:
    """Сохранить авторов в JSON."""
    return save_list(filename, [
        {"id": author.id, "name": author.name, "email": author.email}
        for author in authors
    ])


def load_news(
    authors: list[Author], filename: Path = NEWS_FILE
) -> list[News]:
    """Загрузить новости и связать каждую с объектом Author по author_id."""
    news = []
    for data in load_list(filename):
        try:
            author = get_author_by_id(authors, data["author_id"])
            if author is None:
                print(f"Новость {data['id']} пропущена: нет автора "
                      f"с id {data['author_id']}.")
                continue
            news.append(News(
                data["id"],
                data["title"],
                data["text"],
                author,
                data["category"],
                data.get("views", 0),
                data.get("pub_date", ""),
            ))
        except (KeyError, TypeError, ValueError):
            print(f"Пропущена битая запись новости: {data}")
    return news


def save_news(news: list[News], filename: Path = NEWS_FILE) -> bool:
    """Сохранить новости в JSON (вместо объекта автора пишется author_id)."""
    return save_list(filename, [
        {
            "id": item.id,
            "title": item.title,
            "text": item.text,
            "author_id": item.author.id,
            "category": item.category,
            "views": item.views,
            "pub_date": item.pub_date,
        }
        for item in news
    ])


def load_comments(
    news: list[News], filename: Path = COMMENTS_FILE
) -> list[Comment]:
    """Загрузить комментарии и связать каждый с объектом News по news_id."""
    comments = []
    for data in load_list(filename):
        try:
            news_item = get_news_by_id(news, data["news_id"])
            if news_item is None:
                print(f"Комментарий {data['id']} пропущен: нет новости "
                      f"с id {data['news_id']}.")
                continue
            comments.append(Comment(
                data["id"], news_item, data.get("author", ""), data["text"]
            ))
        except (KeyError, TypeError):
            print(f"Пропущена битая запись комментария: {data}")
    return comments


def save_comments(
    comments: list[Comment], filename: Path = COMMENTS_FILE
) -> bool:
    """Сохранить комментарии в JSON (вместо объекта новости — news_id)."""
    return save_list(filename, [
        {
            "id": comment.id,
            "news_id": comment.news.id,
            "author": comment.author_name,
            "text": comment.text,
        }
        for comment in comments
    ])
