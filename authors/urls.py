from django.urls import path

from . import views

urlpatterns = [
    path("", views.authors_list, name="authors_list"),
    path("<int:author_id>/", views.author_detail, name="author_detail"),
]
