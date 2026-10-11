"""View-функции главной страницы."""

from django.http import HttpRequest, HttpResponse


def index(request: HttpRequest) -> HttpResponse:
    """Главная страница."""
    return HttpResponse("Система публикации новостей")
