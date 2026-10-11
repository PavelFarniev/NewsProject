"""Главная страница, общий каркас страниц и обработчик ошибки 404."""

from django.http import HttpRequest, HttpResponse

from storage import load_authors, load_comments, load_news

BOOTSTRAP_CSS = (
    "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3"
    "/dist/css/bootstrap.min.css"
)

# Немного своего CSS поверх Bootstrap.
STYLE = """
    body { background-color: #f4f5f7; }
    main { padding-top: 1.5rem; padding-bottom: 2rem; }
    .news-text { white-space: pre-line; font-size: 1.1rem; }
    .list-group-item a { text-decoration: none; }
    footer { color: #6c757d; font-size: 0.9rem; }
"""


def page(title: str, content: str) -> str:
    """Собрать HTML-страницу: head, Bootstrap, навигация и content."""
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{title}</title>
    <link rel="stylesheet" href="{BOOTSTRAP_CSS}">
    <style>{STYLE}</style>
</head>
<body>
    <nav class="navbar navbar-expand bg-dark" data-bs-theme="dark">
        <div class="container">
            <a class="navbar-brand" href="/">Новости</a>
            <div class="navbar-nav">
                <a class="nav-link" href="/">Главная</a>
                <a class="nav-link" href="/news/">Лента</a>
                <a class="nav-link" href="/authors/">Авторы</a>
            </div>
        </div>
    </nav>
    <main class="container">{content}</main>
    <footer class="container pb-3">Система публикации новостей</footer>
</body>
</html>"""


def index(request: HttpRequest) -> HttpResponse:
    """Главная страница: описание проекта, немного цифр и ссылки."""
    authors = load_authors()
    news = load_news(authors)
    comments = load_comments(news)
    content = f"""
    <div class="p-4 mb-4 bg-white rounded-3 shadow-sm">
        <h1 class="display-5">Система публикации новостей</h1>
        <p class="lead">Авторы публикуют новости, а читатели их читают
        и обсуждают в комментариях.</p>
        <a href="/news/" class="btn btn-primary me-2">Лента новостей</a>
        <a href="/authors/" class="btn btn-secondary">Авторы</a>
    </div>
    <div class="row text-center">
        <div class="col">
            <div class="card"><div class="card-body">
                <h2>{len(news)}</h2><p class="mb-0">новостей</p>
            </div></div>
        </div>
        <div class="col">
            <div class="card"><div class="card-body">
                <h2>{len(authors)}</h2><p class="mb-0">авторов</p>
            </div></div>
        </div>
        <div class="col">
            <div class="card"><div class="card-body">
                <h2>{len(comments)}</h2><p class="mb-0">комментариев</p>
            </div></div>
        </div>
    </div>
    """
    return HttpResponse(page("Система публикации новостей", content))


def page_not_found(request: HttpRequest, exception: Exception) -> HttpResponse:
    """Своя страница 404 (подключена через handler404 в корневом urls.py)."""
    content = """
    <h1 class="text-danger">404 — страница не найдена</h1>
    <p>Проверьте адрес или вернитесь на главную.</p>
    <a href="/" class="btn btn-primary">На главную</a>
    """
    return HttpResponse(
        page("404 — страница не найдена", content),
        status=404,
    )
