"""View-функции раздела новостей.

Данные берутся из JSON средствами ПР3: storage.py загружает объекты
Author, News и Comment, а функции из models/ ищут нужные.
"""

from django.http import HttpRequest, HttpResponse
from django.utils.html import escape

from homepage.views import page
from models import News
from models.comments import get_comments_for_news
from models.news import filter_news_by_category, get_news_by_id, sort_news
from storage import load_authors, load_comments, load_news
from utils import format_date

POPULARITY_BADGES = {
    "ВИРУСНАЯ (очень популярная)": "bg-danger",
    "ПОПУЛЯРНАЯ": "bg-warning text-dark",
    "НОВАЯ (мало просмотров)": "bg-secondary",
}


def news_list(request: HttpRequest) -> HttpResponse:
    """Лента новостей, сначала свежие. ?category=Спорт — фильтр."""
    authors = load_authors()
    news = sort_news(load_news(authors), key="date")
    category = request.GET.get("category", "")
    if category:
        news = list(filter_news_by_category(news, category))

    buttons = '<a href="/news/" class="btn btn-sm btn-outline-dark me-1">'
    buttons += "Все</a>"
    for name in News.CATEGORIES + (News.DEFAULT_CATEGORY,):
        buttons += (
            f'<a href="/news/?category={name}" '
            f'class="btn btn-sm btn-outline-primary me-1">{name}</a>'
        )

    items = ""
    for item in news:
        items += f"""
        <li class="list-group-item d-flex justify-content-between">
            <div>
                <a href="/news/{item.id}/" class="fw-semibold">
                    {escape(item.title)}</a>
                <div class="small text-muted">
                    {format_date(item.pub_date)} ·
                    <a href="/authors/{item.author.id}/">
                        {escape(item.author.name)}</a>
                </div>
            </div>
            <div class="text-end">
                <span class="badge bg-primary">{item.category}</span>
                <div class="small text-muted">{item.views} просм.</div>
            </div>
        </li>"""
    if not items:
        items = '<li class="list-group-item">Новостей нет.</li>'

    content = f"""
    <h1>Лента новостей</h1>
    <div class="mb-3">{buttons}</div>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page("Лента новостей", content))


def news_detail(request: HttpRequest, news_id: int) -> HttpResponse:
    """Страница новости с автором и комментариями; нет новости — 404."""
    authors = load_authors()
    news = load_news(authors)
    item = get_news_by_id(news, news_id)

    if item is None:
        content = """
        <h1 class="text-danger">Новость не найдена</h1>
        <a href="/news/" class="btn btn-outline-secondary">
            ← к ленте новостей
        </a>
        """
        return HttpResponse(
            page("Новость не найдена", content),
            status=404,
        )

    comments = get_comments_for_news(load_comments(news), item)
    comments_html = ""
    for comment in comments:
        comments_html += (
            f'<li class="list-group-item">{escape(str(comment))}</li>'
        )
    if not comments_html:
        comments_html = (
            '<li class="list-group-item text-muted">'
            "Комментариев пока нет.</li>"
        )

    popularity = item.popularity()
    badge = POPULARITY_BADGES.get(popularity, "bg-secondary")
    content = f"""
    <div class="card mb-4">
        <div class="card-body">
            <span class="badge bg-primary mb-2">{item.category}</span>
            <h1 class="card-title h3">{escape(item.title)}</h1>
            <p class="text-muted">
                {format_date(item.pub_date)} · автор:
                <a href="/authors/{item.author.id}/">
                    {escape(item.author.name)}</a>
            </p>
            <p class="news-text">{escape(item.text)}</p>
            <p class="card-text">
                Просмотров: {item.views}
                <span class="badge {badge}">{popularity}</span>
            </p>
            <a href="/news/" class="btn btn-outline-secondary">
                ← к ленте новостей
            </a>
        </div>
    </div>
    <h2 class="h5">Комментарии ({len(comments)})</h2>
    <ul class="list-group">{comments_html}</ul>
    """
    return HttpResponse(page(item.title, content), status=200)
