"""Класс News и функции для работы со списком новостей."""

from collections.abc import Iterator

from utils import next_id, today_iso

from .authors import Author


class News:
    """Новость: заголовок, текст, автор, категория и просмотры."""

    CATEGORIES: tuple[str, ...] = (
        "Технологии",
        "Спорт",
        "Политика",
        "Культура",
    )
    DEFAULT_CATEGORY = "Разное"

    def __init__(
        self,
        news_id: int,
        title: str,
        text: str,
        author: Author,
        category: str,
        views: int = 0,
        pub_date: str = "",
    ) -> None:
        """Создать новость. Автор хранится как объект Author."""
        if views < 0:
            raise ValueError("Число просмотров не может быть меньше нуля.")
        self.id = news_id
        self.title = title
        self.text = text
        self.author = author
        self.category = News.normalize_category(category)
        self.pub_date = pub_date
        self._views = views

    @staticmethod
    def normalize_category(category: str) -> str:
        """Категория из списка или «Разное» (assign_category из ПР1)."""
        normalized = category.strip().capitalize()
        if normalized in News.CATEGORIES:
            return normalized
        return News.DEFAULT_CATEGORY

    @property
    def views(self) -> int:
        """Число просмотров. Менять его можно только через register_view()."""
        return self._views

    def register_view(self) -> int:
        """Засчитать один просмотр и вернуть новое число просмотров."""
        self._views += 1
        return self._views

    def popularity(self) -> str:
        """Оценка популярности по просмотрам (rate_popularity из ПР1)."""
        if self._views >= 1000:
            return "ВИРУСНАЯ (очень популярная)"
        if self._views >= 100:
            return "ПОПУЛЯРНАЯ"
        return "НОВАЯ (мало просмотров)"

    def matches(self, query: str) -> bool:
        """Есть ли query в заголовке или тексте (без учета регистра)."""
        needle = query.strip().lower()
        return needle in self.title.lower() or needle in self.text.lower()

    def __str__(self) -> str:
        """Короткое описание новости для списков."""
        return (
            f"[{self.id}] {self.title} — {self.author.name}, "
            f"{self.category}"
        )


def publish_news(title: str, text: str, author: str) -> str:
    """Проверить поля новости и вернуть текстовый статус (функция из ПР1)."""
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


def create_news(
    news: list[News],
    title: str,
    text: str,
    author: Author | None,
    category: str,
    views: int = 0,
    pub_date: str | None = None,
) -> News:
    """Создать объект News, добавить его в список и вернуть.

    Если данные неправильные, выбрасывается ValueError с текстом ошибки.
    """
    author_name = author.name if author else ""
    status = publish_news(title.strip(), text.strip(), author_name)
    if status.startswith("Ошибка"):
        raise ValueError(status)
    item = News(
        next_id(news),
        title.strip(),
        text.strip(),
        author,
        category,
        views,
        pub_date or today_iso(),
    )
    news.append(item)
    return item


def get_news_by_id(news: list[News], news_id: int) -> News | None:
    """Найти новость по id; если ее нет, вернуть None."""
    return next((item for item in news if item.id == news_id), None)


def find_news(news: list[News], query: str) -> list[News]:
    """Найти новости, где query есть в заголовке или тексте."""
    return [item for item in news if item.matches(query)]


def filter_news_by_category(news: list[News], category: str) -> Iterator[News]:
    """Генератор: по одной выдает новости нужной категории."""
    wanted = News.normalize_category(category)
    for item in news:
        if item.category == wanted:
            yield item


def sort_news(
    news: list[News], key: str = "views", reverse: bool = True
) -> list[News]:
    """Вернуть отсортированную копию списка.

    key: "views" — по просмотрам, "date" — по дате, "title" — по заголовку.
    """
    key_functions = {
        "views": lambda item: item.views,
        "date": lambda item: item.pub_date,
        "title": lambda item: item.title.lower(),
    }
    if key not in key_functions:
        raise ValueError(f"Неизвестный ключ сортировки: {key}")
    return sorted(news, key=key_functions[key], reverse=reverse)


def delete_news(news: list[News], news_id: int) -> News | None:
    """Удалить новость из списка и вернуть ее (или None, если не нашли)."""
    item = get_news_by_id(news, news_id)
    if item is not None:
        news.remove(item)
    return item


def get_statistics(news: list[News]) -> dict:
    """Статистика: число новостей, просмотров, авторов, категории, топ."""
    by_category: dict[str, int] = {}
    total_views = 0
    for item in news:
        by_category[item.category] = by_category.get(item.category, 0) + 1
        total_views += item.views
    return {
        "total": len(news),
        "total_views": total_views,
        "by_category": by_category,
        "authors": len({item.author.id for item in news}),
        "most_popular": max(news, key=lambda item: item.views, default=None),
    }
