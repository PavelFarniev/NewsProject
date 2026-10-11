"""View-функции раздела новостей."""

from django.http import HttpRequest, HttpResponse


def news_list(request: HttpRequest) -> HttpResponse:
    """Список новостей."""
    return HttpResponse("Список новостей")


def news_detail(request: HttpRequest, news_id: int) -> HttpResponse:
    """Страница одной новости."""
    return HttpResponse(f"Новость {news_id}")
