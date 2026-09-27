"""Сохранение и загрузка данных приложения в JSON-файлах."""

import json
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"
NEWS_FILE = DATA_DIR / "news.json"
COMMENTS_FILE = DATA_DIR / "comments.json"


def load_list(filename: Path) -> list[dict]:
    """Загрузить список словарей из JSON-файла.

    При отсутствии файла или некорректном содержимом возвращается
    пустой список, а пользователь получает сообщение об ошибке.
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
    """Сохранить список словарей в JSON-файл.

    Возвращает True при успешной записи и False при ошибке.
    """
    try:
        filename.parent.mkdir(parents=True, exist_ok=True)
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(items, file, ensure_ascii=False, indent=4)
    except OSError as error:
        print(f"Не удалось сохранить {filename.name}: {error}")
        return False
    return True


def load_news(filename: Path = NEWS_FILE) -> list[dict]:
    """Загрузить новости из JSON-файла."""
    return load_list(filename)


def save_news(news: list[dict], filename: Path = NEWS_FILE) -> bool:
    """Сохранить новости в JSON-файл."""
    return save_list(filename, news)


def load_comments(filename: Path = COMMENTS_FILE) -> list[dict]:
    """Загрузить комментарии из JSON-файла."""
    return load_list(filename)


def save_comments(
    comments: list[dict], filename: Path = COMMENTS_FILE
) -> bool:
    """Сохранить комментарии в JSON-файл."""
    return save_list(filename, comments)
