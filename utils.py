"""Вспомогательные функции: безопасный ввод и форматирование."""

from datetime import date


def input_int(prompt: str, min_value: int = 0) -> int:
    """Запросить у пользователя целое число не меньше min_value.

    При некорректном вводе запрос повторяется.
    """
    while True:
        raw_value = input(prompt).strip()
        try:
            value = int(raw_value)
        except ValueError:
            print("Ошибка: введите целое число.")
            continue
        if value < min_value:
            print(f"Ошибка: число должно быть не меньше {min_value}.")
            continue
        return value


def input_text(prompt: str, allow_empty: bool = False) -> str:
    """Запросить строку; пустой ввод повторяется, если он запрещен."""
    while True:
        value = input(prompt).strip()
        if value or allow_empty:
            return value
        print("Ошибка: значение не может быть пустым.")


def next_id(items: list[dict]) -> int:
    """Вернуть следующий свободный идентификатор для списка записей."""
    return max((item["id"] for item in items), default=0) + 1


def today_iso() -> str:
    """Вернуть текущую дату в формате ГГГГ-ММ-ДД."""
    return date.today().isoformat()


def format_date(iso_date: str) -> str:
    """Преобразовать дату из ГГГГ-ММ-ДД в ДД.ММ.ГГГГ.

    Если строка не является датой, она возвращается без изменений.
    """
    try:
        return date.fromisoformat(iso_date).strftime("%d.%m.%Y")
    except ValueError:
        return iso_date
