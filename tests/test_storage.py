"""Тесты сохранения и загрузки JSON-файлов."""

from storage import load_list, save_list


def test_save_and_load(tmp_path):
    filename = tmp_path / "news.json"
    items = [{"id": 1, "title": "Новость"}]
    assert save_list(filename, items)
    assert load_list(filename) == items


def test_load_missing_file(tmp_path):
    assert load_list(tmp_path / "missing.json") == []


def test_load_broken_json(tmp_path):
    filename = tmp_path / "broken.json"
    filename.write_text("{не json", encoding="utf-8")
    assert load_list(filename) == []
