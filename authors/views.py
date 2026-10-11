"""View-функции раздела авторов."""

from django.http import HttpRequest, HttpResponse
from django.utils.html import escape

from homepage.views import page
from models.authors import get_author_by_id
from storage import load_authors, load_news
from utils import format_date


def authors_list(request: HttpRequest) -> HttpResponse:
    """Список авторов и сколько новостей у каждого."""
    authors = load_authors()
    news = load_news(authors)
    items = ""
    for author in authors:
        count = len([item for item in news if item.author is author])
        items += f"""
        <li class="list-group-item d-flex justify-content-between">
            <a href="/authors/{author.id}/">{escape(author.name)}</a>
            <span class="badge bg-secondary">{count} нов.</span>
        </li>"""
    if not items:
        items = '<li class="list-group-item">Авторов нет.</li>'
    content = f"""
    <h1>Авторы</h1>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page("Авторы", content))


def author_detail(request: HttpRequest, author_id: int) -> HttpResponse:
    """Карточка автора и его новости; если автора нет — 404."""
    authors = load_authors()
    author = get_author_by_id(authors, author_id)
    if author is None:
        content = """
        <h1 class="text-danger">Автор не найден</h1>
        <a href="/authors/" class="btn btn-outline-secondary">
            ← к списку авторов
        </a>
        """
        return HttpResponse(page("Автор не найден", content), status=404)

    news = [item for item in load_news(authors) if item.author is author]
    items = ""
    for item in news:
        items += f"""
        <li class="list-group-item">
            <a href="/news/{item.id}/">{escape(item.title)}</a>
            <span class="text-muted small">
                · {format_date(item.pub_date)}</span>
        </li>"""
    if not items:
        items = '<li class="list-group-item text-muted">Новостей нет.</li>'
    email = escape(author.email) if author.email else "не указана"
    content = f"""
    <div class="card mb-4">
        <div class="card-body">
            <h1 class="card-title h3">{escape(author.name)}</h1>
            <p class="card-text"><strong>ID:</strong> {author.id}</p>
            <p class="card-text"><strong>Почта:</strong> {email}</p>
            <a href="/authors/" class="btn btn-outline-secondary">
                ← к списку авторов
            </a>
        </div>
    </div>
    <h2 class="h5">Новости автора ({len(news)})</h2>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page(author.name, content), status=200)
