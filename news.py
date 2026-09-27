"""Функции работы с новостями: публикация, поиск, сортировка, статистика.

Функции publish_news(), assign_category() и rate_popularity()
перенесены из начального сценария ПР1.
"""

from collections.abc import Iterator

from utils import next_id, today_iso

ALLOWED_CATEGORIES: tuple[str, ...] = (
    "Технологии",
    "Спорт",
    "Политика",
    "Культура",
)
DEFAULT_CATEGORY = "Разное"
SORT_KEYS: tuple[str, ...] = ("views", "date", "title")


def publish_news(title: str, text: str, author: str) -> str:
    """Проверить поля новости и вернуть текстовый статус публикации (ПР1)."""
    if len(title) == 0:
        return "Ошибка: Заголовок не может быть пустым. Публикация отменена."
    if len(text) == 0:
        return (
            "Ошибка: Текст новости не может быть пустым. "
            "Публикация отменена."
        )
    if len(author) == 0:
        return "Ошибка: Не указан автор. Публикация отменена."
    return f"Новость успешно опубликована автором {author}."


def assign_category(category: str) -> str:
    """Вернуть категорию из списка разрешенных или «Разное» (ПР1).

    В ПР1 разрешенные категории хранились строкой, что допускало
    частичные совпадения; теперь используется кортеж.
    """
    normalized = category.strip().capitalize()
    if normalized in ALLOWED_CATEGORIES:
        return normalized
    return DEFAULT_CATEGORY


def rate_popularity(views: int) -> str:
    """Оценить популярность новости по числу просмотров (ПР1)."""
    if views >= 1000:
        return "ВИРУСНАЯ (очень популярная)"
    elif views >= 100:
        return "ПОПУЛЯРНАЯ"
    else:
        return "НОВАЯ (мало просмотров)"


def create_news(
    news: list[dict],
    title: str,
    text: str,
    author: str,
    category: str,
    views: int = 0,
    pub_date: str | None = None,
) -> dict:
    """Создать новость и добавить ее в список news.

    Возвращает словарь созданной новости. При некорректных данных
    выбрасывает ValueError с текстом из publish_news().
    """
    status = publish_news(title.strip(), text.strip(), author.strip())
    if status.startswith("Ошибка"):
        raise ValueError(status)
    if views < 0:
        raise ValueError("Ошибка: число просмотров не может быть < 0.")
    item = {
        "id": next_id(news),
        "title": title.strip(),
        "text": text.strip(),
        "author": author.strip(),
        "category": assign_category(category),
        "views": views,
        "pub_date": pub_date or today_iso(),
    }
    news.append(item)
    return item


def get_news_by_id(news: list[dict], news_id: int) -> dict | None:
    """Найти новость по идентификатору; вернуть None, если ее нет."""
    return next((item for item in news if item["id"] == news_id), None)


def find_news(news: list[dict], query: str) -> list[dict]:
    """Найти новости, в заголовке или тексте которых есть подстрока query.

    Поиск выполняется без учета регистра.
    """
    needle = query.strip().lower()
    found = []
    for item in news:
        if needle in item["title"].lower() or needle in item["text"].lower():
            found.append(item)
    return found


def filter_news_by_category(
    news: list[dict], category: str
) -> Iterator[dict]:
    """Генератор новостей указанной категории."""
    wanted = assign_category(category)
    for item in news:
        if item["category"] == wanted:
            yield item


def sort_news(
    news: list[dict], key: str = "views", reverse: bool = True
) -> list[dict]:
    """Вернуть новый список новостей, отсортированный по ключу.

    key: "views" — по просмотрам, "date" — по дате, "title" — по заголовку.
    """
    key_functions = {
        "views": lambda item: item["views"],
        "date": lambda item: item["pub_date"],
        "title": lambda item: item["title"].lower(),
    }
    if key not in key_functions:
        raise ValueError(f"Неизвестный ключ сортировки: {key}")
    return sorted(news, key=key_functions[key], reverse=reverse)


def register_view(news: list[dict], news_id: int) -> int:
    """Увеличить счетчик просмотров новости и вернуть новое значение.

    Если новости нет, выбрасывается KeyError.
    """
    item = get_news_by_id(news, news_id)
    if item is None:
        raise KeyError(news_id)
    item["views"] += 1
    return item["views"]


def delete_news(news: list[dict], comments: list[dict], news_id: int) -> bool:
    """Удалить новость и все комментарии к ней.

    Возвращает True, если новость была найдена и удалена.
    """
    item = get_news_by_id(news, news_id)
    if item is None:
        return False
    news.remove(item)
    comments[:] = [c for c in comments if c["news_id"] != news_id]
    return True


def get_statistics(news: list[dict]) -> dict:
    """Собрать статистику по новостям.

    Возвращает словарь: общее число новостей, сумму просмотров,
    количество новостей по категориям, число авторов и самую
    популярную новость.
    """
    by_category: dict[str, int] = {}
    total_views = 0
    for item in news:
        category = item["category"]
        by_category[category] = by_category.get(category, 0) + 1
        total_views += item["views"]
    most_popular = max(news, key=lambda item: item["views"], default=None)
    return {
        "total": len(news),
        "total_views": total_views,
        "by_category": by_category,
        "authors": len({item["author"] for item in news}),
        "most_popular": most_popular,
    }
