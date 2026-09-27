"""Точка запуска приложения «Система публикации новостей»."""

import inspect
from collections.abc import Callable

from models import Author, Comment, News
from models.authors import add_author, find_author, get_author_by_id
from models.comments import (
    add_comment,
    delete_comment,
    delete_comments_for_news,
    get_comments_for_news,
)
from models.news import (
    create_news,
    delete_news,
    filter_news_by_category,
    find_news,
    get_news_by_id,
    get_statistics,
    sort_news,
)
from storage import (
    load_authors,
    load_comments,
    load_news,
    save_authors,
    save_comments,
    save_news,
)
from utils import format_date, input_int, input_text

Action = Callable[[list[Author], list[News], list[Comment]], bool]
CATEGORIES_HINT = "/".join(News.CATEGORIES)


def show_news_list(news: list[News]) -> None:
    """Вывести новости таблицей."""
    if not news:
        print("Новостей нет.")
        return
    print(f"{'ID':>3}  {'Дата':<10}  {'Просм.':>6}  {'Категория':<11}  "
          "Заголовок (автор)")
    for item in news:
        print(f"{item.id:>3}  {format_date(item.pub_date):<10}  "
              f"{item.views:>6}  {item.category:<11}  "
              f"{item.title} ({item.author.name})")


def show_news_details(item: News, comments: list[Comment]) -> None:
    """Вывести новость целиком вместе с комментариями."""
    print("                НОВОСТНАЯ ЛЕНТА")
    print(f"ЗАГОЛОВОК : {item.title}")
    print(f"АВТОР     : {item.author}")
    print(f"КАТЕГОРИЯ : {item.category}")
    print(f"ДАТА      : {format_date(item.pub_date)}")
    print(f"ПРОСМОТРЫ : {item.views} ({item.popularity()})")
    print("ТЕКСТ НОВОСТИ:")
    print(item.text)
    print("КОММЕНТАРИИ:")
    news_comments = get_comments_for_news(comments, item)
    if not news_comments:
        print("Комментариев пока нет.")
    for comment in news_comments:
        print(f"  [{comment.id}] {comment}")


def show_authors(authors: list[Author]) -> None:
    """Вывести список авторов."""
    if not authors:
        print("Авторов нет.")
    for author in authors:
        print(f"{author.id:>3}. {author}")


def action_show_feed(
    authors: list[Author], news: list[News], comments: list[Comment]
) -> bool:
    """Показать ленту новостей (сначала свежие)."""
    show_news_list(sort_news(news, key="date"))
    return False


def action_open_news(
    authors: list[Author], news: list[News], comments: list[Comment]
) -> bool:
    """Открыть новость по ID и засчитать просмотр."""
    news_id = input_int("ID новости: ", min_value=1)
    item = get_news_by_id(news, news_id)
    if item is None:
        print(f"Новость с ID {news_id} не найдена.")
        return False
    item.register_view()
    show_news_details(item, comments)
    return True


def action_publish(
    authors: list[Author], news: list[News], comments: list[Comment]
) -> bool:
    """Опубликовать новость от имени одного из авторов."""
    show_authors(authors)
    author_id = input_int("ID автора: ", min_value=1)
    author = get_author_by_id(authors, author_id)
    if author is None:
        print(f"Автор с ID {author_id} не найден. Сначала добавьте автора.")
        return False
    title = input_text("Заголовок: ", allow_empty=True)
    text = input_text("Текст: ", allow_empty=True)
    category = input_text(f"Категория ({CATEGORIES_HINT}): ",
                          allow_empty=True)
    try:
        item = create_news(news, title, text, author, category)
    except ValueError as error:
        print(error)
        return False
    print(f"Новость опубликована: {item}")
    return True


def action_search(
    authors: list[Author], news: list[News], comments: list[Comment]
) -> bool:
    """Найти новости по слову из заголовка или текста."""
    show_news_list(find_news(news, input_text("Что ищем: ")))
    return False


def action_by_category(
    authors: list[Author], news: list[News], comments: list[Comment]
) -> bool:
    """Показать новости выбранной категории."""
    category = input_text(f"Категория ({CATEGORIES_HINT}): ")
    show_news_list(list(filter_news_by_category(news, category)))
    return False


def action_sort(
    authors: list[Author], news: list[News], comments: list[Comment]
) -> bool:
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


def action_add_comment(
    authors: list[Author], news: list[News], comments: list[Comment]
) -> bool:
    """Добавить комментарий к новости."""
    news_id = input_int("ID новости: ", min_value=1)
    item = get_news_by_id(news, news_id)
    if item is None:
        print(f"Новость с ID {news_id} не найдена.")
        return False
    author_name = input_text("Ваше имя (Enter — аноним): ", allow_empty=True)
    text = input_text("Комментарий: ", allow_empty=True)
    try:
        add_comment(comments, item, author_name, text)
    except ValueError as error:
        print(error)
        return False
    print("Комментарий добавлен.")
    return True


def action_delete_comment(
    authors: list[Author], news: list[News], comments: list[Comment]
) -> bool:
    """Удалить комментарий по ID."""
    comment_id = input_int("ID комментария: ", min_value=1)
    if delete_comment(comments, comment_id):
        print("Комментарий удален.")
        return True
    print(f"Комментарий с ID {comment_id} не найден.")
    return False


def action_delete_news(
    authors: list[Author], news: list[News], comments: list[Comment]
) -> bool:
    """Удалить новость вместе с комментариями к ней."""
    news_id = input_int("ID новости: ", min_value=1)
    item = delete_news(news, news_id)
    if item is None:
        print(f"Новость с ID {news_id} не найдена.")
        return False
    removed = delete_comments_for_news(comments, item)
    print(f"Новость удалена (и комментариев к ней: {removed}).")
    return True


def action_show_authors(
    authors: list[Author], news: list[News], comments: list[Comment]
) -> bool:
    """Показать всех авторов."""
    show_authors(authors)
    return False


def action_add_author(
    authors: list[Author], news: list[News], comments: list[Comment]
) -> bool:
    """Добавить нового автора."""
    name = input_text("Имя автора: ", allow_empty=True)
    email = input_text("Почта (можно пропустить): ", allow_empty=True)
    try:
        author = add_author(authors, name, email)
    except ValueError as error:
        print(error)
        return False
    print(f"Автор добавлен: {author} (ID {author.id})")
    return True


def action_find_author(
    authors: list[Author], news: list[News], comments: list[Comment]
) -> bool:
    """Найти автора по имени или почте и показать его новости."""
    found = find_author(authors, input_text("Имя или почта: "))
    if not found:
        print("Никого не нашли.")
    for author in found:
        print(f"{author.id:>3}. {author}")
        show_news_list([item for item in news if item.author is author])
    return False


def action_statistics(
    authors: list[Author], news: list[News], comments: list[Comment]
) -> bool:
    """Показать статистику по новостям."""
    stats = get_statistics(news)
    print(f"Всего новостей: {stats['total']}")
    print(f"Всего просмотров: {stats['total_views']}")
    print(f"Авторов с публикациями: {stats['authors']} из {len(authors)}")
    print(f"Комментариев: {len(comments)}")
    for category, count in stats["by_category"].items():
        print(f"  {category}: {count}")
    if stats["most_popular"]:
        print(f"Самая популярная: «{stats['most_popular'].title}»")
    return False


def action_help(
    authors: list[Author], news: list[News], comments: list[Comment]
) -> bool:
    """Справка по пунктам меню (описания берутся из docstring)."""
    for key, (title, action) in MENU.items():
        doc = inspect.getdoc(action) or "нет описания"
        print(f"{key}. {title}: {doc}")
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
    "10": ("Показать авторов", action_show_authors),
    "11": ("Добавить автора", action_add_author),
    "12": ("Найти автора", action_find_author),
    "13": ("Статистика", action_statistics),
    "14": ("Справка", action_help),
}


def print_menu() -> None:
    """Вывести меню."""
    print("\n=== Система публикации новостей ===")
    for key, (title, _) in MENU.items():
        print(f"{key}. {title}")
    print("0. Выход")


def save_all(
    authors: list[Author], news: list[News], comments: list[Comment]
) -> None:
    """Сохранить все данные в JSON-файлы."""
    save_authors(authors)
    save_news(news)
    save_comments(comments)


def main() -> None:
    """Загрузить данные и крутить меню, пока пользователь не выйдет."""
    authors = load_authors()
    news = load_news(authors)
    comments = load_comments(news)
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
        if action(authors, news, comments):
            save_all(authors, news, comments)
    print("До свидания!")


if __name__ == "__main__":
    main()
