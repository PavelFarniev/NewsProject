"""Корневые маршруты проекта: адреса распределяются по приложениям."""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("homepage.urls")),
    path("news/", include("news.urls")),
    path("authors/", include("authors.urls")),
]

# Своя страница 404. Работает, когда DEBUG = False.
handler404 = "homepage.views.page_not_found"
