"""Класс News и функции для работы со списком новостей."""

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
