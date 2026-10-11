"""Корневые маршруты проекта: адреса распределяются по приложениям."""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("homepage.urls")),
    path("news/", include("news.urls")),
    path("authors/", include("authors.urls")),
]
