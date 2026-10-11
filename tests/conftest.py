"""Настройка Django перед запуском тестов веб-части."""

import os

import django
from django.test.utils import setup_test_environment


def pytest_configure() -> None:
    """Подключить настройки newsportal, чтобы работал тестовый Client."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "newsportal.settings")
    django.setup()
    setup_test_environment()
