"""Точка запуска приложения «Система публикации новостей»."""

import inspect
from collections.abc import Callable

from comments import (
    add_comment,
    delete_comment,
    format_comment,
    get_comments_for_news,
)
from news import (
    ALLOWED_CATEGORIES,
    create_news,
    delete_news,
    filter_news_by_category,
    find_news,
    get_news_by_id,
    get_statistics,
    rate_popularity,
    register_view,
    sort_news,
)
from storage import load_comments, load_news, save_comments, save_news
from utils import format_date, input_int, input_text

Action = Callable[[list[dict], list[dict]], bool]


def show_news_list(news: list[dict]) -> None:
    """Вывести список новостей в виде таблицы."""
    if not news:
        print("Новостей нет.")
        return
    print(f"{'ID':>3}  {'Дата':<10}  {'Просм.':>6}  {'Категория':<11}  "
          "Заголовок")
    for item in news:
        print(f"{item['id']:>3}  {format_date(item['pub_date']):<10}  "
              f"{item['views']:>6}  {item['category']:<11}  {item['title']}")


def show_news_details(item: dict, comments: list[dict]) -> None:
    """Вывести новость полностью вместе с комментариями (развитие ПР1)."""
    print("                НОВОСТНАЯ ЛЕНТА")
    print(f"ЗАГОЛОВОК : {item['title']}")
    print(f"АВТОР     : {item['author']}")
    print(f"КАТЕГОРИЯ : {item['category']}")
    print(f"ДАТА      : {format_date(item['pub_date'])}")
    print(f"ПРОСМОТРЫ : {item['views']} ({rate_popularity(item['views'])})")
    print("ТЕКСТ НОВОСТИ:")
    print(item["text"])
    print("КОММЕНТАРИИ:")
    news_comments = get_comments_for_news(comments, item["id"])
    if not news_comments:
        print(format_comment("", ""))
    for comment in news_comments:
        text = format_comment(comment["text"], comment["author"])
        print(f"  [{comment['id']}] {text}")


def action_show_feed(news: list[dict], comments: list[dict]) -> bool:
    """Показать ленту новостей (сначала свежие)."""
    show_news_list(sort_news(news, key="date"))
    return False


def action_open_news(news: list[dict], comments: list[dict]) -> bool:
    """Открыть новость по ID и засчитать просмотр."""
    news_id = input_int("ID новости: ", min_value=1)
    try:
        register_view(news, news_id)
    except KeyError:
        print(f"Новость с ID {news_id} не найдена.")
        return False
    show_news_details(get_news_by_id(news, news_id), comments)
    return True


def action_publish(news: list[dict], comments: list[dict]) -> bool:
    """Опубликовать новую новость."""
    title = input_text("Заголовок: ", allow_empty=True)
    text = input_text("Текст: ", allow_empty=True)
    author = input_text("Автор: ", allow_empty=True)
    category = input_text(
        f"Категория ({'/'.join(ALLOWED_CATEGORIES)}): ", allow_empty=True
    )
    try:
        item = create_news(news, title, text, author, category)
    except ValueError as error:
        print(error)
        return False
    print(f"Новость успешно опубликована автором {item['author']} "
          f"(ID {item['id']}, категория «{item['category']}»).")
    return True


def action_search(news: list[dict], comments: list[dict]) -> bool:
    """Найти новости по подстроке в заголовке или тексте."""
    query = input_text("Что ищем: ")
    show_news_list(find_news(news, query))
    return False


def action_by_category(news: list[dict], comments: list[dict]) -> bool:
    """Показать новости выбранной категории."""
    category = input_text(f"Категория ({'/'.join(ALLOWED_CATEGORIES)}): ")
    show_news_list(list(filter_news_by_category(news, category)))
    return False


def action_sort(news: list[dict], comments: list[dict]) -> bool:
    """Показать ленту, отсортированную по выбранному признаку."""
    print("1 — по просмотрам, 2 — по дате, 3 — по заголовку")
    choice = input_int("Способ сортировки: ", min_value=1)
    keys = {1: ("views", True), 2: ("date", True), 3: ("title", False)}
    if choice not in keys:
        print("Нет такого способа сортировки.")
        return False
    key, reverse = keys[choice]
    show_news_list(sort_news(news, key=key, reverse=reverse))
    return False


def action_add_comment(news: list[dict], comments: list[dict]) -> bool:
    """Добавить комментарий к новости."""
    news_id = input_int("ID новости: ", min_value=1)
    author = input_text("Ваше имя (Enter — аноним): ", allow_empty=True)
    text = input_text("Комментарий: ", allow_empty=True)
    try:
        add_comment(comments, news, news_id, author, text)
    except KeyError:
        print(f"Новость с ID {news_id} не найдена.")
        return False
    except ValueError as error:
        print(error)
        return False
    print("Комментарий добавлен.")
    return True


def action_delete_comment(news: list[dict], comments: list[dict]) -> bool:
    """Удалить комментарий по ID."""
    comment_id = input_int("ID комментария: ", min_value=1)
    if delete_comment(comments, comment_id):
        print("Комментарий удален.")
        return True
    print(f"Комментарий с ID {comment_id} не найден.")
    return False


def action_delete_news(news: list[dict], comments: list[dict]) -> bool:
    """Удалить новость вместе с комментариями."""
    news_id = input_int("ID новости: ", min_value=1)
    if delete_news(news, comments, news_id):
        print("Новость и комментарии к ней удалены.")
        return True
    print(f"Новость с ID {news_id} не найдена.")
    return False


def action_statistics(news: list[dict], comments: list[dict]) -> bool:
    """Показать статистику по новостям."""
    stats = get_statistics(news)
    print(f"Всего новостей: {stats['total']}")
    print(f"Всего просмотров: {stats['total_views']}")
    print(f"Авторов: {stats['authors']}")
    print(f"Комментариев: {len(comments)}")
    for category, count in stats["by_category"].items():
        print(f"  {category}: {count}")
    if stats["most_popular"]:
        print(f"Самая популярная: «{stats['most_popular']['title']}»")
    return False


def action_help(news: list[dict], comments: list[dict]) -> bool:
    """Справка: описание пунктов меню, полученное через интроспекцию."""
    for key, (title, action) in MENU.items():
        doc = inspect.getdoc(action) or "нет описания"
        print(f"{key}. {title}: {action.__name__}() — {doc}")
    return False


MENU: dict[str, tuple[str, Action]] = {
    "1": ("Показать ленту новостей", action_show_feed),
    "2": ("Открыть новость", action_open_news),
    "3": ("Опубликовать новость", action_publish),
    "4": ("Найти новость", action_search),
    "5": ("Новости по категории", action_by_category),
    "6": ("Сортировать ленту", action_sort),
    "7": ("Добавить комментарий", action_add_comment),
    "8": ("Удалить комментарий", action_delete_comment),
    "9": ("Удалить новость", action_delete_news),
    "10": ("Статистика", action_statistics),
    "11": ("Справка", action_help),
}


def print_menu() -> None:
    """Вывести меню приложения."""
    print("\n=== Система публикации новостей ===")
    for key, (title, _) in MENU.items():
        print(f"{key}. {title}")
    print("0. Выход")


def main() -> None:
    """Точка запуска: загрузка данных и основной цикл меню."""
    news = load_news()
    comments = load_comments()
    while True:
        print_menu()
        try:
            choice = input("Выберите действие: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if choice == "0":
            break
        if choice not in MENU:
            print("Нет такого пункта меню.")
            continue
        _, action = MENU[choice]
        if action(news, comments):
            save_news(news)
            save_comments(comments)
    print("До свидания!")


if __name__ == "__main__":
    main()
