"""View-функции раздела авторов."""

from django.http import HttpRequest, HttpResponse


def authors_list(request: HttpRequest) -> HttpResponse:
    """Список авторов."""
    return HttpResponse("Список авторов")


def author_detail(request: HttpRequest, author_id: int) -> HttpResponse:
    """Страница одного автора."""
    return HttpResponse(f"Автор {author_id}")
