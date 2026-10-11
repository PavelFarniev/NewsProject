"""Тесты веб-страниц: URL -> view -> HTTP-ответ."""

import pytest
from django.test import Client, override_settings
from django.urls import resolve, reverse


@pytest.fixture
def client() -> Client:
    return Client()


@pytest.mark.parametrize("url", [
    "/", "/news/", "/news/1/", "/authors/", "/authors/1/",
    "/news/?category=Спорт",
])
def test_pages_open(client, url):
    response = client.get(url)
    assert response.status_code == 200
    assert "bootstrap" in response.content.decode()


@pytest.mark.parametrize("url", ["/news/999/", "/authors/999/"])
def test_missing_objects_give_404(client, url):
    assert client.get(url).status_code == 404


def test_converter_int_rejects_text(client):
    # /news/abc/ не подходит под <int:news_id>, view даже не вызывается
    assert client.get("/news/abc/").status_code == 404


def test_url_resolves_to_view():
    match = resolve("/news/1/")
    assert match.func.__name__ == "news_detail"
    assert match.kwargs == {"news_id": 1}
    assert reverse("author_detail", args=[2]) == "/authors/2/"


def test_news_page_shows_object_data(client):
    html = client.get("/news/1/").content.decode()
    assert "Открыт новый технопарк" in html
    assert "Иван Петров" in html
    assert "Комментарии" in html


def test_custom_404_page(client):
    with override_settings(DEBUG=False):
        response = client.get("/nonexistent/")
    assert response.status_code == 404
    assert "404 — страница не найдена" in response.content.decode()
